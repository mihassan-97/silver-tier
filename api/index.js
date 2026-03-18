export default function handler(req, res) {
  res.status(200).json({ ok: true, message: "Silver Tier Personal AI Employee is running.", health: "/api/health" });
}
