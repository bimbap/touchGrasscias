# touchGrasscias 🌱

> **GitHub Heatmap Reforestation & Activity Synthesis Engine**  
> *"Touch grass digitally, maintain the green streak perpetually."*

---

## 🎯 Purpose
`touchGrasscias` ensures your GitHub contribution heatmap stays consistently active, vibrant green, and free from awkward historical activity voids.

It features two complementary engines:
1. **Cloud Autonomous Reforestation Bot (GitHub Actions)**: 24/7 background scheduler making 1–3 realistic commits multiple times per day directly on GitHub's infrastructure without keeping your PC awake.
2. **Local Retroactive Seeder CLI (`scripts/backfill.py`)**: Powerful backdating generator to heal historical empty months (e.g. past gaps in your heatmap) with realistic, customizable density.

---

## ⚙️ Quick Start

### 1. Enable GitHub Profile Contribution Tracking
To ensure your commits appear on your public profile graph (especially if this repository is private):
1. Navigate to your GitHub Profile (`https://github.com/bimbap`).
2. Above your contribution graph, click **Contribution settings** (top-right dropdown).
3. Ensure **"Include private contributions in your profile"** is checked.
4. Also verify in **Settings -> Emails** that `[EMAIL_ADDRESS]` is linked to your account.

### 2. Autonomous Cloud Bot (GitHub Actions)
The bot is preconfigured in `.github/workflows/reforestation.yml`:
- **Schedule**: Runs automatically at UTC 03:00, 09:00, 15:00, and 21:00.
- **Pulse Intensity**: Randomly creates 1 to 3 micro-commits per trigger with realistic commit messages.
- **Manual Trigger**: You can trigger it instantly at any time from the **Actions** tab on GitHub by clicking **Run workflow**.

> **Note on GitHub Actions Permissions**:  
> In your repository, go to **Settings** -> **Actions** -> **General** -> scroll down to **Workflow permissions** -> ensure **"Read and write permissions"** is selected.

---

### 3. Retroactive Historical Seeder (`scripts/backfill.py`)
To fill past empty gaps (such as the November–March blank spots on your profile):

```bash
# Preview what will be generated (no changes made)
python scripts/backfill.py --dry-run

# Custom date range with organic density
python scripts/backfill.py --start-date 2025-11-01 --end-date 2026-04-01 --intensity organic

# Deep neon green intensity for maximum color
python scripts/backfill.py --start-date 2025-11-01 --end-date 2026-03-31 --intensity high
```

After generating commits, simply push to GitHub:
```bash
git push origin main
```
Your GitHub contribution tiles will immediately reflect the new green blocks!

---