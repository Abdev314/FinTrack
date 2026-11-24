#!/usr/bin/env python3
"""Generate FinTrack report diagrams using Graphviz."""
from pathlib import Path
import graphviz

DOCS = Path(__file__).parent


def generate_flowchart():
    dot = graphviz.Digraph(
        name="FinTrack Flowchart",
        filename=str(DOCS / "flowchart"),
        format="png",
        graph_attr={"rankdir": "TB", "bgcolor": "white", "fontname": "Helvetica"},
        node_attr={"shape": "box", "style": "rounded,filled", "fontname": "Helvetica", "fontsize": "12"},
        edge_attr={"fontname": "Helvetica", "fontsize": "11"},
    )

    # Nodes
    dot.node("start", "User opens FinTrack", fillcolor="#e0e7ff", shape="oval")
    dot.node("dashboard", "Dashboard loads\n(fetch all records)", fillcolor="#c7d2fe")
    dot.node("display", "Display summary cards\n& records table", fillcolor="#dbeafe")
    dot.node("add", "Add Record", fillcolor="#d1fae5")
    dot.node("edit", "Edit Record", fillcolor="#fef3c7")
    dot.node("search", "Search Records", fillcolor="#e0e7ff")
    dot.node("export", "Export Records", fillcolor="#fce7f3")
    dot.node("delete", "Delete Record", fillcolor="#fee2e2")
    dot.node("api", "REST API\n(JAX-RS / Jersey)", fillcolor="#bfdbfe")
    dot.node("service", "RecordService\n(business logic)", fillcolor="#a5b4fc")
    dot.node("repo", "RecordRepositoryImpl\n(Hibernate/JPA)", fillcolor="#93c5fd")
    dot.node("db", "PostgreSQL\n(records table)", fillcolor="#67e8f9", shape="cylinder")
    dot.node("refresh", "Refresh dashboard", fillcolor="#c7d2fe")

    # Edges
    dot.edge("start", "dashboard")
    dot.edge("dashboard", "display")
    dot.edge("display", "add", label=" + Add")
    dot.edge("display", "edit", label=" ✎ Edit")
    dot.edge("display", "search", label=" 🔍 Search")
    dot.edge("display", "export", label=" ⬇ Export")
    dot.edge("display", "delete", label=" 🗑 Delete")

    for action in ["add", "edit", "search", "export", "delete"]:
        dot.edge(action, "api")

    dot.edge("api", "service")
    dot.edge("service", "repo")
    dot.edge("repo", "db")
    dot.edge("db", "repo")
    dot.edge("repo", "service")
    dot.edge("service", "api")
    dot.edge("api", "refresh")
    dot.edge("refresh", "display")

    dot.render(cleanup=True)
    print(f"Flowchart saved to {DOCS / 'flowchart.png'}")


def generate_erd():
    dot = graphviz.Digraph(
        name="FinTrack ERD",
        filename=str(DOCS / "erd"),
        format="png",
        graph_attr={"rankdir": "LR", "bgcolor": "white", "fontname": "Helvetica"},
        node_attr={"shape": "plaintext", "fontname": "Helvetica", "fontsize": "12"},
        edge_attr={"fontname": "Helvetica"},
    )

    entity_label = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8" BGCOLOR="#f8fafc">
      <TR><TD COLSPAN="2" BGCOLOR="#4f46e5" ALIGN="CENTER"><FONT COLOR="white"><B>records</B></FONT></TD></TR>
      <TR><TD BGCOLOR="#e0e7ff" ALIGN="LEFT"><B>record_id</B></TD><TD BGCOLOR="#e0e7ff" ALIGN="LEFT">VARCHAR (PK)</TD></TR>
      <TR><TD ALIGN="LEFT">transaction_type</TD><TD ALIGN="LEFT">VARCHAR (ENUM)</TD></TR>
      <TR><TD ALIGN="LEFT">amount</TD><TD ALIGN="LEFT">INTEGER</TD></TR>
      <TR><TD ALIGN="LEFT">transaction_category</TD><TD ALIGN="LEFT">VARCHAR (ENUM)</TD></TR>
      <TR><TD ALIGN="LEFT">record_date</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
      <TR><TD ALIGN="LEFT">operator</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
      <TR><TD ALIGN="LEFT">notes</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
    </TABLE>
    >"""

    enum_type_label = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" BGCOLOR="#f8fafc">
      <TR><TD BGCOLOR="#10b981" ALIGN="CENTER"><FONT COLOR="white"><B>TransactionType</B></FONT></TD></TR>
      <TR><TD ALIGN="CENTER">INCOME</TD></TR>
      <TR><TD ALIGN="CENTER">EXPENSE</TD></TR>
      <TR><TD ALIGN="CENTER">TRANSFER</TD></TR>
    </TABLE>
    >"""

    enum_cat_label = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" BGCOLOR="#f8fafc">
      <TR><TD BGCOLOR="#f59e0b" ALIGN="CENTER"><FONT COLOR="white"><B>TransactionCategory</B></FONT></TD></TR>
      <TR><TD ALIGN="CENTER">SALARY</TD></TR>
      <TR><TD ALIGN="CENTER">RENT</TD></TR>
      <TR><TD ALIGN="CENTER">TRANSPORT</TD></TR>
      <TR><TD ALIGN="CENTER">SHOPPING</TD></TR>
      <TR><TD ALIGN="CENTER">FOOD</TD></TR>
      <TR><TD ALIGN="CENTER">ENTERTAINMENT</TD></TR>
      <TR><TD ALIGN="CENTER">OTHER</TD></TR>
    </TABLE>
    >"""

    dot.node("records", entity_label)
    dot.node("transaction_type", enum_type_label)
    dot.node("transaction_category", enum_cat_label)

    dot.edge("records", "transaction_type", label="uses", arrowhead="none", style="dashed", color="#64748b")
    dot.edge("records", "transaction_category", label="uses", arrowhead="none", style="dashed", color="#64748b")

    dot.render(cleanup=True)
    print(f"ERD saved to {DOCS / 'erd.png'}")


if __name__ == "__main__":
    generate_flowchart()
    generate_erd()
