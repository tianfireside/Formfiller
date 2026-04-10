"""
BC SCCR Form 2 — Response to Civil Claim
"""


def replace_text(para, old, new, bold=None):
    if old not in para.text:
        return False
    for run in para.runs:
        if old in run.text:
            if bold is None:
                run.text = run.text.replace(old, new)
            else:
                # Split into label (keep formatting) + value (new formatting)
                before = run.text[: run.text.index(old)]
                run.text = before
                new_run = para.add_run(new)
                new_run.bold = bold
            return True
    full = para.text.replace(old, new)
    for run in para.runs:
        run.text = ""
    if para.runs:
        para.runs[0].text = full
    else:
        para.add_run(full)
    return True


def fill(doc, firm, matter):
    replacements = {
        "{{address}}":     (firm["address"],     False),
        "{{fax}}":         (firm["fax"],         False),
        "{{email}}":       (firm["email"],        False),
        "{{lawyer_name}}": (firm["lawyer_name"],  None),
    }

    for para in doc.paragraphs:
        for placeholder, (value, bold) in replacements.items():
            replace_text(para, placeholder, value, bold=bold)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for placeholder, (value, bold) in replacements.items():
                        replace_text(para, placeholder, value, bold=bold)
