# pages/documentation.py - Niv Louie web app user guide

from html import escape
from pathlib import Path
import re

from nicegui import ui

GUIDE_FILENAME = "niv_louie_web_documentation.md"

MAIN_SECTIONS = (
    ("introduction", "Introduction to Niv Louie"),
    ("spreadsheet", "Building your spreadsheet"),
    ("sign-in", "Signing in and the dashboard"),
    ("create-project", "Creating a new project"),
    ("edit-project", "Editing or removing a project"),
    ("braille-document", "Creating a braille document"),
    ("nvda-addon", "Creating an NVDA add-on"),
    ("liblouis-table", "Creating a Liblouis table"),
    ("yaml-test", "Creating a YAML test for Liblouis"),
    ("collaborate", "Collaborate"),
    ("files", "Where your files live"),
)

_SKIP_H2_TITLES = {"table of contents", "contents"}

_MD_ANCHORS = {
    "#1-introduction-to-niv-louie": "#introduction",
    "#2-building-your-spreadsheet": "#spreadsheet",
    "#3-signing-in-and-the-dashboard": "#sign-in",
    "#4-creating-a-new-project": "#create-project",
    "#5-editing-or-removing-a-project": "#edit-project",
    "#6-creating-a-braille-document": "#braille-document",
    "#7-creating-an-nvda-add-on": "#nvda-addon",
    "#8-creating-a-liblouis-table": "#liblouis-table",
    "#9-creating-a-yaml-test-for-liblouis": "#yaml-test",
    "#10-collaborate": "#collaborate",
    "#11-where-your-files-live": "#files",
}


def _guide_candidates():
    root = Path(__file__).resolve().parent.parent
    return [
        root / "static" / GUIDE_FILENAME,
        root / "static" / "docs" / GUIDE_FILENAME,
        Path("/app/static") / GUIDE_FILENAME,
        Path("/app/static/docs") / GUIDE_FILENAME,
    ]


def _find_guide_path():
    for path in _guide_candidates():
        if path.is_file():
            return path
    return None


def _normalize_heading(title):
    return re.sub(r"^\d+\.\s*", "", title).strip().lower()


def _id_for_h2(title):
    normalized = _normalize_heading(title)
    for section_id, label in MAIN_SECTIONS:
        if normalized == label.lower():
            return section_id
    return None


def _rewrite_md_links(text):
    for old, new in _MD_ANCHORS.items():
        text = text.replace(old, new)
    return text


def _clean_body(lines):
    text = "\n".join(lines).strip()
    if text.startswith("---"):
        text = text[3:].strip()
    if text.endswith("---"):
        text = text[:-3].strip()
    body_lines = text.split("\n")
    while body_lines:
        last = body_lines[-1].strip()
        if last.startswith("©") or last == "---" or last == "":
            body_lines.pop()
            continue
        break
    return "\n".join(body_lines).strip()


def _first_paragraph(text):
    for block in text.split("\n\n"):
        paragraph = block.strip()
        if paragraph and paragraph != "---":
            return paragraph
    return ""


def _parse_guide(markdown):
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    intro_lines = []
    sections = []
    current = None
    in_code = False
    skipping_toc = False

    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            if current is not None and not skipping_toc:
                current["body"].append(line)
            continue

        heading = None if in_code else re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if level == 1:
                continue
            if level == 2:
                skipping_toc = _normalize_heading(title) in _SKIP_H2_TITLES
                if skipping_toc:
                    if current is not None:
                        sections.append(current)
                        current = None
                    continue
                if current is not None:
                    sections.append(current)
                current = {"title": title, "body": []}
                continue

        if skipping_toc:
            continue
        if current is None:
            if stripped == "---":
                continue
            intro_lines.append(line)
        else:
            current["body"].append(line)

    if current is not None:
        sections.append(current)

    intro = _first_paragraph("\n".join(intro_lines).strip())
    parsed = []
    for section in sections:
        parsed.append({
            "title": section["title"],
            "id": _id_for_h2(section["title"]),
            "body": _rewrite_md_links(_clean_body(section["body"])),
        })
    return intro, parsed


def _render_missing_guide():
    print(f"LOG: User guide file not found: {GUIDE_FILENAME}")
    ui.label("The user guide file was not found.").classes("text-lg text-gray-700")


def _render_guide(intro, sections):
    if intro:
        ui.markdown(intro).classes("text-lg leading-relaxed")

    toc_items = "\n".join(
        f'<li><a href="#{escape(section_id, quote=True)}">{escape(label)}</a></li>'
        for section_id, label in MAIN_SECTIONS
    )
    ui.html(
        f'''<nav aria-labelledby="on-this-page">
            <h2 id="on-this-page" class="text-2xl font-semibold mb-4 text-primary">On this page</h2>
            <ul class="list-disc pl-6 space-y-2">
                {toc_items}
            </ul>
        </nav>''',
        sanitize=False,
    ).classes("w-full my-8")

    for section in sections:
        heading_id = section["id"]
        title = escape(section["title"])
        if heading_id:
            heading_html = (
                f'<h2 id="{escape(heading_id, quote=True)}" '
                f'class="text-2xl font-semibold mt-10 mb-4 text-primary">{title}</h2>'
            )
        else:
            heading_html = (
                f'<h2 class="text-2xl font-semibold mt-10 mb-4 text-primary">{title}</h2>'
            )
        ui.html(heading_html, sanitize=False)
        if section["body"]:
            ui.markdown(section["body"]).classes("text-base leading-relaxed documentation-guide-body")


@ui.page("/documentation")
def documentation():
    ui.query(".nicegui-content").classes("w-full")
    ui.query(".q-page").classes("flex flex-col min-h-screen")
    ui.add_css("""
        .documentation-guide h2,
        .documentation-guide h3 {
            scroll-margin-top: 5rem;
        }
        .documentation-guide-body table {
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }
        .documentation-guide-body th,
        .documentation-guide-body td {
            border: 1px solid #d1d5db;
            padding: 0.5rem 0.75rem;
            text-align: left;
        }
        .documentation-guide-body pre {
            overflow-x: auto;
        }
    """)

    ui.add_head_html(
        '<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">'
    )

    with ui.header().classes("items-center justify-between bg-primary text-white p-4 shadow"):
        with ui.row().classes("items-center gap-6 w-full max-w-6xl mx-auto"):
            ui.label("Niv Louie").classes("text-3xl font-bold tracking-tight")
            ui.space()
            ui.button("Home", on_click=lambda: ui.navigate.to("/")).props("flat color=accent")
            ui.button(
                "Go to Dashboard",
                on_click=lambda: ui.navigate.to("/dashboard"),
            ).props("flat color=accent")

    with ui.column().classes("documentation-guide flex-1 w-full max-w-4xl mx-auto p-8 gap-4"):
        ui.html(
            '<h1 class="text-4xl font-bold text-primary">Niv Louie user guide</h1>',
            sanitize=False,
        )

        guide_path = _find_guide_path()
        if guide_path is None:
            _render_missing_guide()
        else:
            print(f"LOG: Serving user guide from {guide_path}")
            markdown = guide_path.read_text(encoding="utf-8")
            intro, sections = _parse_guide(markdown)
            _render_guide(intro, sections)

    with ui.column().classes("w-full bg-gray-100 py-12 border-t mt-auto"):
        ui.label("© 2026 Niv Louie - Free and Open Source (GPL-3.0)").classes(
            "text-xs text-gray-500 text-center mx-auto"
        )
