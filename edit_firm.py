#!/usr/bin/env python3
"""
edit_firm.py — Update your firm's information in firm.json
Usage: python edit_firm.py
"""

import json
import os

FIRM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "firm.json")


def main():
    print("\n" + "=" * 50)
    print("  Firm Information Editor")
    print("=" * 50)

    # Load existing data
    with open(FIRM_FILE, "r") as f:
        firm = json.load(f)

    print("\nPress Enter to keep the current value.\n")

    for field, current in firm.items():
        label = field.replace("_", " ").title()
        display = current if current else "(empty)"
        new_val = input(f"  {label} [{display}]: ").strip()
        if new_val:
            firm[field] = new_val

    # Save updated data
    with open(FIRM_FILE, "w") as f:
        json.dump(firm, f, indent=4)

    print("\n  Saved.\n")


if __name__ == "__main__":
    main()
