## 🥚 Egg Incubator Tracker (Terminal Edition)

A fully terminal-based egg incubation tracker with persistent history, visual progress, and milestone alerts — all without a GUI. Designed for hatchers, homesteaders, and biohacking poultry enthusiasts.

### 🔧 Features

* ⏱ Track 8 eggs in a visual 2x4 grid, updated with age and estimated hatch date (21 days).
* 🎨 Color-coded progress milestones: 7d (yellow), 14d (cyan), 18d (blinking red), 21d+ (green).
* 📝 Persistent state and action logging (`incubator_data.json` + `incubator_log.txt`).
* 🧑‍💻 Interactive menu or one-liner terminal commands:

  * `python incubator.py` (menu)
  * `python incubator.py show`
  * `python incubator.py add 3 06-15`
  * `python incubator.py remove 3`
* 🗖 Accepts multiple date formats (month-first supported):

  * `YYYY-MM-DD`, `MM-DD-YYYY`, `MM/DD/YYYY`, `MM-DD`, `MM/DD`
* ⛔ Validates against future dates.

### 🐍 Requirements

* Python 3.6+
* ANSI-compatible terminal (most modern terminals are fine)

### 🚀 Usage

```bash
# Show grid view once
python incubator.py show

# Add egg to slot 4 (today's date)
python incubator.py add 4

# Add egg with specific date
python incubator.py add 5 06/01/2025

# Remove egg from slot 2
python incubator.py remove 2

# Start interactive menu
python incubator.py

# View help
python incubator.py help
```
****
