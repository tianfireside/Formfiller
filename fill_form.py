#!/usr/bin/env python3
"""
fill_form.py — Fireside Law Form Filler
Usage: python fill_form.py
"""

import json
import os
from docx import Document

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FIRM_FILE = os.path.join(BASE_DIR, "data", "firm.json")

# Map (court_folder, form_number) -> handler module
FORM_HANDLERS = {
    ("SCCR", 2): "forms.bc_sccr_form2",
}


def load_firm():
    if not os.path.exists(FIRM_FILE):
        print("\n  Error: firm.json not found. Run edit_firm.py first.\n")
        exit(1)
    with open(FIRM_FILE, "r") as f:
        return json.load(f)


def select_court():
    templates_dir = os.path.join(BASE_DIR, "templates")
    courts = sorted([d for d in os.listdir(templates_dir)
                     if os.path.isdir(os.path.join(templates_dir, d))])
    if not courts:
        print("\n  Error: no courts found in templates/.\n")
        exit(1)

    print("\n  Which court?")
    for i, court in enumerate(courts, 1):
        print(f"    ({i}) {court}")

    choice = input("\n  Enter number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(courts)):
        print("\n  Invalid choice.\n")
        exit(1)

    return courts[int(choice) - 1]


def parse_form_number(filename):
    """Extract the number from FORM2_... -> 2"""
    name = os.path.splitext(filename)[0]
    part = name.split("_")[0].upper()
    if part.startswith("FORM") and part[4:].isdigit():
        return int(part[4:])
    return None


def select_form(court):
    court_dir = os.path.join(BASE_DIR, "templates", court)
    forms = sorted([f for f in os.listdir(court_dir) if f.endswith(".docx")])
    if not forms:
        print(f"\n  Error: no forms found in templates/{court}/.\n")
        exit(1)

    form_map = {}
    print(f"\n  Which form?")
    for form in forms:
        num = parse_form_number(form)
        if num:
            form_map[num] = form
            print(f"    ({num}) {form}")
        else:
            print(f"    (?) {form}")

    choice = input("\n  Enter number: ").strip()
    if not choice.isdigit() or int(choice) not in form_map:
        print("\n  Invalid choice.\n")
        exit(1)

    return int(choice), os.path.join(BASE_DIR, "templates", court, form_map[int(choice)])


def main():
    firm = load_firm()

    matter = input("\n  Matter number: ").strip()
    if not matter:
        print("\n  Error: matter number is required.\n")
        exit(1)

    court         = select_court()
    form_num, template = select_form(court)

    doc = Document(template)

    # Route to the right form handler
    key = (court, form_num)
    if key not in FORM_HANDLERS:
        print(f"\n  Error: no handler found for {court} Form {form_num}.\n")
        exit(1)

    import importlib
    handler = importlib.import_module(FORM_HANDLERS[key])
    handler.fill(doc, firm, matter)

    # Save output
    matter_dir = os.path.join(BASE_DIR, "output", f"M{matter}")
    os.makedirs(matter_dir, exist_ok=True)

    form_name = os.path.splitext(os.path.basename(template))[0]
    out_name  = f"draft_M{matter}_{form_name}.docx"
    out_path  = os.path.join(matter_dir, out_name)
    doc.save(out_path)
    print(f"\n  Saved → {out_path}\n")


if __name__ == "__main__":
    main()
