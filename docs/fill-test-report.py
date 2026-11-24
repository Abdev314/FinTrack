#!/usr/bin/env python3
"""Fill docs/Test_report.docx (test plan template) with the FinTrack test plan content."""
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

DOCS = Path(__file__).parent
DOCX = DOCS / "Test_report.docx"

BULLET_NUM_ID = "1"  # bullet list defined in the template's numbering.xml
GITHUB_URL = "https://github.com/Abdev314/FinTrack"

doc = Document(DOCX)


def find_paragraph(text):
    for p in doc.paragraphs:
        if p.text.strip() == text:
            return p
    raise LookupError(f"paragraph not found: {text!r}")


def delete_paragraph(paragraph):
    paragraph._p.getparent().remove(paragraph._p)


def make_bullet(paragraph):
    paragraph.style = doc.styles["List Paragraph"]
    pPr = paragraph._p.get_or_add_pPr()
    numPr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numId = OxmlElement("w:numId")
    numId.set(qn("w:val"), BULLET_NUM_ID)
    numPr.append(ilvl)
    numPr.append(numId)
    pPr.append(numPr)


def add_hyperlink(paragraph, url, text):
    r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.append(color)
    rPr.append(underline)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def set_table_borders(table):
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    table._tbl.tblPr.append(borders)


def add_table_before(anchor, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    for j, header in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = header
        for run in cell.paragraphs[0].runs:
            run.bold = True
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row):
            table.rows[i].cells[j].text = value
    set_table_borders(table)
    anchor._p.addprevious(table._tbl)


def fill_section(placeholder_text, blocks):
    anchor = find_paragraph(placeholder_text)
    for block in blocks:
        kind = block[0]
        if kind == "p":
            anchor.insert_paragraph_before(block[1])
        elif kind == "b":
            make_bullet(anchor.insert_paragraph_before(block[1]))
        elif kind == "strong":
            new_p = anchor.insert_paragraph_before()
            new_p.add_run(block[1]).bold = True
        elif kind == "table":
            add_table_before(anchor, block[1], block[2])
    delete_paragraph(anchor)


# ---------- header fields (label/value table at the top of the document) ----------
HEADER_VALUES = {
    "Student Name:": "[Your full name]",
    "Student ID:": "[Your student ID]",
    "Date:": "September 14, 2026",
    "Class:": "[Your class]",
}
header_table = doc.tables[0]
for row in header_table.rows:
    for idx, cell in enumerate(row.cells[:-1]):
        label = cell.text.strip()
        if label in HEADER_VALUES:
            row.cells[idx + 1].text = HEADER_VALUES[label]

# GitHub repository row in the header table
repo_row = header_table.add_row()
label_cell = repo_row.cells[0]
value_cell = repo_row.cells[1].merge(repo_row.cells[3])
label_cell.text = "GitHub Repository:"
for run in label_cell.paragraphs[0].runs:
    run.bold = True
tcPr = label_cell._tc.get_or_add_tcPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear")
shd.set(qn("w:fill"), "D6EAF8")
tcPr.append(shd)
value_cell.text = ""
add_hyperlink(value_cell.paragraphs[0], GITHUB_URL, GITHUB_URL)

# ---------- remove template instructions ----------
delete_paragraph(find_paragraph("Instructions"))
delete_paragraph(
    find_paragraph(
        "Select a real or simulated project and write a complete test plan using the structure below."
    )
)

# ---------- 1. Introduction ----------
fill_section(
    "[Describe the project background, purpose, and scope of this test plan]",
    [
        ("p", "FinTrack is a web-based personal finance application that lets users record, view, "
              "search, and delete income and expense transactions, and export their records to PDF or "
              "Excel. The system consists of a Java JAX-RS (Jersey 2.40) REST backend packaged as a WAR "
              "(FinTrack 1.0-SNAPSHOT) and deployed at http://localhost:8080/FinTrack, a PostgreSQL "
              "database accessed through Hibernate 5.6 / JPA 2.2, and a Vue 3 + TypeScript single-page "
              "frontend built with Vite. The source code is publicly available at "
              "https://github.com/Abdev314/FinTrack."),
        ("p", "The purpose of this document is to define the scope, strategy, environment, schedule, "
              "resources, and risks for testing FinTrack before release. The scope covers the REST API "
              "endpoints under /api/records and the corresponding frontend features; items outside this "
              "scope are listed in Section 4."),
    ],
)

# ---------- 2. Test Items ----------
fill_section(
    "[List the software items/features under test and their versions]",
    [
        ("b", "Backend WAR — FinTrack 1.0-SNAPSHOT (com.web.fintrack): RecordResource (REST endpoints), "
              "RecordService (validation logic), RecordRepositoryImpl (JPA data access), Record entity, "
              "TransactionType and TransactionCategory enums, IllegalArgumentExceptionMapper"),
        ("b", "Frontend SPA — Vue 3.5 + TypeScript + Vite: Home page, AddRecordForm, EditRecordForm, "
              "SearchRecord, and DownloadRecord components, and the recordApi HTTP service"),
        ("b", "Database — records table in PostgreSQL 15 (run via docker-compose.yml)"),
        ("b", "Test basis — test-commands.md (cURL test suite), docs/erd.png, docs/flowchart.png"),
    ],
)

# ---------- 3. Features to be Tested ----------
fill_section(
    "[List features in scope for testing]",
    [
        ("strong", "Record creation (POST /api/records)"),
        ("b", "Creating a record with valid data returns 201 Created with a Location header and "
              "persists the record in the database"),
        ("b", "Validation rejections: null record, blank recordId, duplicate recordId, amount \u2264 0, "
              "or missing transactionType, with the error message returned in the response body"),
        ("strong", "Record retrieval (GET endpoints)"),
        ("b", "GET /api/records returns all records; GET /api/records/{id} returns 200 with the record "
              "or 404 when it does not exist"),
        ("b", "Filtering by transaction type (GET /api/records/type/{type}) and by category "
              "(GET /api/records/category/{category})"),
        ("strong", "Record deletion (DELETE /api/records/{id})"),
        ("b", "Successful deletion returns 204 No Content; a subsequent GET of the same ID returns 404"),
        ("strong", "Frontend features"),
        ("b", "Add record form, edit record flow (implemented as delete + create), search/filter, "
              "record list rendering, and PDF/Excel export"),
    ],
)

# ---------- 4. Features Not to be Tested ----------
fill_section(
    "[List features explicitly out of scope and explain why]",
    [
        ("b", "True record update (PUT/PATCH) — no update endpoint exists in the API; editing is "
              "emulated by the frontend as delete + create, so only that workaround flow is tested"),
        ("b", "Authentication and authorization — not implemented in this version"),
        ("b", "Performance, load, and concurrency testing — FinTrack is a single-user application in "
              "this release"),
        ("b", "Third-party libraries (Jersey, Hibernate, jsPDF, jspdf-autotable, xlsx) — exercised only "
              "indirectly through integration-level testing"),
        ("b", "Cross-browser compatibility — the UI is verified in the development browser only"),
    ],
)

# ---------- 5. Test Strategy / Approach ----------
fill_section(
    "[Describe testing methods, types, levels, and techniques to be used]",
    [
        ("p", "Testing is performed at the system level, primarily manual and black-box: the backend is "
              "exercised over HTTP and the frontend through the browser. JUnit 5 is already declared as "
              "a test dependency in pom.xml, and unit tests for the RecordService validation logic will "
              "be added; until then, the cURL suite in test-commands.md is the main executable test basis."),
        ("b", "API functional testing with cURL/Postman, verifying HTTP status codes (201, 200, 204, "
              "404) and JSON payloads against the Record model"),
        ("b", "Boundary value analysis and equivalence partitioning on the amount field (zero, "
              "negative, small, large values) and on recordId, transactionType, and the type/category "
              "path parameters"),
        ("b", "Positive and negative testing of every endpoint, including invalid enum literals in the URL"),
        ("b", "End-to-end UI testing of the forms, search, edit flow, and PDF/Excel export"),
        ("b", "Defect retesting and a full regression pass over the cURL suite after any code change"),
    ],
)

# ---------- 6. Test Environment ----------
fill_section(
    "[Describe hardware, software, network, and tool requirements]",
    [
        ("b", "Hardware: standard x86-64 development workstation (8 GB RAM or more)"),
        ("b", "OS: Linux with a current Chrome or Firefox browser"),
        ("b", "Backend: JDK 17 (per pom.xml), Maven via the mvnw wrapper; WAR deployed to a servlet "
              "container at http://localhost:8080/FinTrack/api"),
        ("b", "Database: PostgreSQL 15 in Docker (docker-compose.yml, host port 5433), psql client for "
              "direct data verification"),
        ("b", "Frontend: Node.js LTS and npm; Vite dev server; API base URL from frontend/.env "
              "(VITE_API_BASE_URL)"),
        ("b", "Tools: cURL or Postman for API calls, browser DevTools for the UI, psql for database checks"),
    ],
)

# ---------- 7. Schedule & Milestones ----------
fill_section(
    "[Define test phases, start/end dates, and milestones]",
    [
        ("p", "Testing is organized into six phases, each with a clear testing focus and milestone:"),
        ("table",
         ["Phase", "Timeline (2026)", "Testing activities", "Milestone"],
         [
             ["1. Planning & environment setup", "Sep 14",
              "Review requirements and design (ERD, flowchart, API code); build the WAR (mvn package); "
              "start PostgreSQL via docker-compose; deploy the backend and start the Vite dev server; "
              "prepare test data (rec-001, rec-002)", "M1: test environment ready"],
             ["2. API functional testing (positive paths)", "Sep 15",
              "Execute happy-path tests: create a record (201 + Location header); GET all / by ID / by "
              "type / by category (200); delete a record (204); verify JSON field mapping against the "
              "Record model", "M2: all endpoints pass positive tests"],
             ["3. API boundary & negative testing", "Sep 16",
              "Boundary and equivalence tests on amount (0, negative, large); blank, missing, and "
              "duplicate recordId; missing transactionType; invalid enum literal in the path; GET and "
              "DELETE on non-existent IDs (404)", "M3: all validation paths verified"],
             ["4. UI / end-to-end testing", "Sep 17",
              "Test AddRecordForm, EditRecordForm (delete + create flow), SearchRecord filters, record "
              "list, and PDF/Excel export in DownloadRecord; verify the UI displays server errors "
              "correctly", "M4: UI features pass E2E scenarios"],
             ["5. Defect retest & regression", "Sep 18",
              "Retest every fixed defect; rerun the full cURL suite (test-commands.md) as regression; "
              "re-verify exports", "M5: no open critical/high defects"],
             ["6. Test report & sign-off", "Sep 18-19",
              "Consolidate results, evaluate entry/exit criteria, finalize and approve the test report",
              "M6: test report approved"],
         ]),
        ("p", "M5 (clean regression run) is a hard gate: the final report is produced only when no "
              "critical or high-severity defects remain open. Any phase slip of more than one day is "
              "reported to the instructor and the schedule is re-baselined."),
    ],
)

# ---------- 8. Resources & Responsibilities ----------
fill_section(
    "[List team members and their roles/responsibilities]",
    [
        ("p", "The project is developed and tested by a single person ([Your Name]), who fulfills all "
              "of the following roles:"),
        ("b", "Test lead / test designer: owns the test plan, test case design, schedule, and the "
              "entry/exit criteria evaluation"),
        ("b", "API tester: executes API, boundary, and negative tests; reports defects"),
        ("b", "UI tester: executes frontend functional and end-to-end tests, including export verification"),
        ("b", "Developer: fixes defects and supports regression runs"),
    ],
)

# ---------- 9. Risks & Contingencies ----------
fill_section(
    "[Identify risks and mitigation strategies]",
    [
        ("table",
         ["Risk", "Impact", "Mitigation / contingency"],
         [
             ["No automated test suite exists, so regression is manual and error-prone", "High",
              "Rerun the full cURL suite (test-commands.md) after every change; prioritize JUnit 5 unit "
              "tests for RecordService validation (dependency already in pom.xml)"],
             ["The edit feature is emulated as delete + create; a failed delete followed by a create can "
              "lose or duplicate data", "Medium",
              "Test the edit flow explicitly, including failure paths, and record the workaround as a "
              "known issue"],
             ["Validation failures return HTTP 404 instead of 400 (IllegalArgumentExceptionMapper), so "
              "clients cannot distinguish 'not found' from 'invalid input'", "Medium",
              "Document as a known issue; verify the frontend handles the 404 response body gracefully"],
             ["Environment unavailable (PostgreSQL container stopped, port conflicts on 8080/5433/5173)",
              "Medium",
              "Run docker-compose up -d before each phase; check port availability during environment "
              "setup (M1)"],
             ["The date field is stored as a free-text String, so invalid date formats can be accepted",
              "Low",
              "Agree expected behavior with the developer and add negative test cases for malformed dates"],
         ]),
    ],
)

# ---------- 10. Entry / Exit Criteria ----------
fill_section(
    "[Define conditions for starting and completing testing]",
    [
        ("strong", "Entry criteria (testing may start when all are true):"),
        ("b", "mvn package builds the WAR cleanly and the application is deployed and reachable at "
              "/api/records"),
        ("b", "PostgreSQL container is running and the records table is available"),
        ("b", "Frontend is served and connected to the backend (VITE_API_BASE_URL verified)"),
        ("b", "Test cases are selected from test-commands.md and extended with boundary/negative cases; "
              "test data (e.g., rec-001, rec-002) is prepared"),
        ("strong", "Exit criteria (testing is complete when all are true):"),
        ("b", "100% of the planned test cases have been executed"),
        ("b", "All failed cases are retested after fixes; no critical or high-severity defects remain open"),
        ("b", "The full cURL regression suite has been rerun and passes"),
        ("b", "Results are documented and the test report is approved"),
    ],
)

doc.save(DOCX)
print(f"Filled {DOCX}")
