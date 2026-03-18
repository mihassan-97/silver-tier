# Personal AI Employee Dashboard

## 🧭 Quick Links
- [Needs Action](./Needs_Action)
- [Plans](./Plans)
- [Pending Approval](./Pending_Approval)
- [Approved](./Approved)
- [Done](./Done)

## 📝 Current Status
- **Tasks pending:**
- **Last run:**

## 🛠️ How to use
1. Drop new notes or emails into `Vault/Needs_Action`
2. Run the processor: `python -m src.claude_agent`
3. Review `Vault/Plans/Plan.md`
4. Approve sensitive actions by moving notes from `Pending_Approval` → `Approved`

## 📌 Notes
- Do not store secrets in the Vault.
- Use `.env` for API keys and credentials.
