
"""
patch_finance_tracker.py

Usage:
    python patch_finance_tracker.py path/to/your_file.py
"""

import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python patch_finance_tracker.py path/to/your_file.py")
    sys.exit(1)

target = Path(sys.argv[1])

if not target.exists():
    print(f"File not found: {target}")
    sys.exit(1)

text = target.read_text(encoding="utf-8")

backup = target.with_suffix(target.suffix + ".bak")
backup.write_text(text, encoding="utf-8")

text = text.replace(
    "return income - expense",
    "return float(np.subtract(income, expense))",
    1
)

text = text.replace(
    'income = df[df["type"]=="income"]["amount"].sum()\n    expense = df[df["type"]=="expense"]["amount"].sum()',
    'income = np.sum(df[df["type"]=="income"]["amount"])\n    expense = np.sum(df[df["type"]=="expense"]["amount"])',
    1
)

target.write_text(text, encoding="utf-8")

print("Patch applied successfully.")
print(f"Backup created: {backup}")
