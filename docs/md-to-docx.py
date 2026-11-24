#!/usr/bin/env python3
"""Convert docs/FinTrack-Report.md into a Word document."""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
import re

DOCS = Path(__file__).parent
MD_PATH = DOCS / "FinTrack-Report.md"
DOCX_PATH = DOCS / "FinTrack-Report.docx"


def add_heading(doc, text, level):
    # Use built-in heading styles
    style = f"Heading {level}"
    p = doc.add_heading(level=level)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p


def add_paragraph(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(11)
    run.bold = bold
    run.italic = italic
    return p


def add_code_block(doc, lines):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("\n".join(lines))
    run.font.name = "Courier New"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p


def add_table_from_lines(doc, lines):
    # lines: list of markdown table rows including separator
    rows = [line.strip() for line in lines if line.strip().startswith("|")]
    if len(rows) < 2:
        return
    # Skip separator row
    data_rows = [rows[0]] + rows[2:]
    cells = [r.strip("|").split("|") for r in data_rows]
    cells = [[c.strip() for c in row] for row in cells]
    if not cells:
        return
    table = doc.add_table(rows=len(cells), cols=len(cells[0]))
    table.style = "Light Grid Accent 1"
    for i, row in enumerate(cells):
        for j, val in enumerate(row):
            table.cell(i, j).text = val
    return table


def add_image(doc, image_path):
    if image_path.exists():
        doc.add_picture(str(image_path), width=Inches(5.5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        add_paragraph(doc, f"[Image not found: {image_path}]")


def parse_markdown(md_text):
    lines = md_text.splitlines()
    i = 0
    blocks = []
    while i < len(lines):
        line = lines[i]
        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            blocks.append(("heading", level, m.group(2)))
            i += 1
            continue
        # Code block
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append(("code", code))
            i += 1
            continue
        # Table
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append(("table", table_lines))
            continue
        # Horizontal rule
        if re.match(r"^\s*[-=]{3,}\s*$", line):
            blocks.append(("hr",))
            i += 1
            continue
        # Image
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line.strip())
        if m:
            blocks.append(("image", m.group(2)))
            i += 1
            continue
        # Normal paragraph / empty
        if line.strip() == "":
            blocks.append(("empty",))
            i += 1
            continue
        # Collect paragraph lines
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith("#") and not lines[i].startswith("|") and not lines[i].strip().startswith("```") and not lines[i].strip().startswith("!"):
            para.append(lines[i])
            i += 1
        blocks.append(("paragraph", "\n".join(para)))
    return blocks


def inline_format(paragraph, text):
    """Apply bold/italic/code formatting within a paragraph text."""
    # Very basic inline parser: handle **bold**, *italic*, `code`
    parts = re.split(r"(\*\*.*?\*\*|\*.*?\*|`[^`]+`)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Courier New"
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        else:
            run = paragraph.add_run(part)
        run.font.name = "Calibri"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
        run.font.size = Pt(11)


def main():
    doc = Document()

    # Default font for the document
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)

    md_text = MD_PATH.read_text(encoding="utf-8")
    blocks = parse_markdown(md_text)

    for block in blocks:
        kind = block[0]
        if kind == "heading":
            _, level, text = block
            add_heading(doc, text, level)
        elif kind == "paragraph":
            _, text = block
            p = doc.add_paragraph()
            inline_format(p, text)
        elif kind == "code":
            _, code = block
            add_code_block(doc, code)
        elif kind == "table":
            _, table_lines = block
            add_table_from_lines(doc, table_lines)
        elif kind == "image":
            _, img = block
            img_path = DOCS / img
            add_image(doc, img_path)
        elif kind == "hr":
            doc.add_paragraph().add_run("_" * 60).font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
        elif kind == "empty":
            continue

    doc.save(DOCX_PATH)
    print(f"Word document saved to {DOCX_PATH}")


if __name__ == "__main__":
    main()
