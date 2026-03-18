"use strict";

const express = require("express");
const bodyParser = require("body-parser");
const nodemailer = require("nodemailer");
const { exec } = require("child_process");
const path = require("path");

require("dotenv").config();

const app = express();
app.use(bodyParser.json());

const PORT = process.env.PORT || 3000;

function createEmailTransport() {
  if (!process.env.EMAIL_SMTP_HOST || !process.env.EMAIL_SMTP_USER || !process.env.EMAIL_SMTP_PASS) {
    throw new Error("Missing SMTP configuration. Set EMAIL_SMTP_HOST, EMAIL_SMTP_USER, EMAIL_SMTP_PASS in .env.");
  }

  return nodemailer.createTransport({
    host: process.env.EMAIL_SMTP_HOST,
    port: Number(process.env.EMAIL_SMTP_PORT || 587),
    secure: false,
    auth: {
      user: process.env.EMAIL_SMTP_USER,
      pass: process.env.EMAIL_SMTP_PASS,
    },
  });
}

app.post("/send-email", async (req, res) => {
  const { to, subject, text, html } = req.body;
  if (!to || !subject || (!text && !html)) {
    return res.status(400).json({ error: "Missing to/subject/text/html" });
  }
  try {
    const transporter = createEmailTransport();
    const info = await transporter.sendMail({
      from: process.env.EMAIL_SMTP_USER,
      to,
      subject,
      text,
      html,
    });
    res.json({ ok: true, info });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false, error: err.message });
  }
});

app.post("/run-action", (req, res) => {
  const { command } = req.body;
  if (!command) {
    return res.status(400).json({ error: "Missing command" });
  }

  exec(command, { cwd: path.resolve(__dirname, "..") }, (err, stdout, stderr) => {
    if (err) {
      return res.status(500).json({ ok: false, error: err.message, stderr });
    }
    res.json({ ok: true, stdout, stderr });
  });
});

app.post("/linkedin-post", async (req, res) => {
  const { content } = req.body;
  if (!content) {
    return res.status(400).json({ error: "Missing content" });
  }

  // Optional: post using Playwright. If credentials are not set, just save the draft.
  const shouldPost = Boolean(process.env.LINKEDIN_EMAIL && process.env.LINKEDIN_PASSWORD);
  if (!shouldPost) {
    return res.json({ ok: true, message: "No LinkedIn credentials provided; not posting." });
  }

  const { chromium } = require("playwright");
  try {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto("https://www.linkedin.com/login");
    await page.fill("input#username", process.env.LINKEDIN_EMAIL);
    await page.fill("input#password", process.env.LINKEDIN_PASSWORD);
    await page.click("button[type=submit]");
    await page.waitForNavigation({ waitUntil: "networkidle" });
    await page.goto("https://www.linkedin.com/feed/");

    // Click create post
    await page.click("button[aria-label='Start a post']");
    await page.waitForSelector("div[role='textbox']", { timeout: 15000 });
    await page.fill("div[role='textbox']", content);

    // Click Post
    await page.click("button[aria-label='Post']");

    await browser.close();
    res.json({ ok: true, message: "Posted to LinkedIn." });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false, error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`MCP server listening on http://localhost:${PORT}`);
});
