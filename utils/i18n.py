"""JSON catalogs for NiceGUI, with per-user language and document direction.

Add a language by placing locales/<code>.json next to the others. The file
must include a "_meta" object with code, native, name, and dir ("ltr" or
"rtl"). No Python change is required. Missing keys fall back to English.
"""

import json
from html import escape
from pathlib import Path

from nicegui import app, ui

LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"
PREFERRED_ORDER = ["en", "he", "ar", "ru", "de", "fr", "es", "it", "zh", "hi"]
DEFAULT_LANGUAGE = "en"

_DIRECTION_CSS = """
<style>
html[dir="rtl"] body,
html[dir="rtl"] .q-page,
html[dir="rtl"] .nicegui-content {
    direction: rtl;
    text-align: start;
}
html[dir="ltr"] body,
html[dir="ltr"] .q-page,
html[dir="ltr"] .nicegui-content {
    direction: ltr;
    text-align: start;
}
html[dir="rtl"] .text-center,
html[dir="ltr"] .text-center {
    text-align: center !important;
}
html[dir="rtl"] .q-field__native,
html[dir="rtl"] input,
html[dir="rtl"] textarea {
    text-align: right;
}
html[dir="rtl"] .font-mono,
html[dir="rtl"] .font-mono .q-field__native {
    direction: ltr;
    text-align: left;
}
.language-switcher {
    min-width: 10rem;
    background: white;
    color: #0B2A4D;
    border-radius: 8px;
}
.language-switcher .q-field__label,
.language-switcher .q-field__native,
.language-switcher .q-select__dropdown-icon {
    color: #0B2A4D !important;
}
</style>
"""


def _load_catalogs():
    languages = {}
    catalogs = {}
    if not LOCALES_DIR.is_dir():
        return languages, catalogs
    for path in sorted(LOCALES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        meta = data.get("_meta") or {}
        code = str(meta.get("code") or path.stem)
        direction = meta.get("dir") if meta.get("dir") in {"ltr", "rtl"} else "ltr"
        languages[code] = {
            "native": str(meta.get("native") or code),
            "name": str(meta.get("name") or code),
            "dir": direction,
        }
        catalogs[code] = {
            key: value
            for key, value in data.items()
            if key != "_meta" and isinstance(value, str)
        }
    return languages, catalogs


LANGUAGES, CATALOGS = _load_catalogs()


def ordered_language_codes():
    codes = list(LANGUAGES)
    codes.sort(key=lambda code: (PREFERRED_ORDER.index(code) if code in PREFERRED_ORDER else len(PREFERRED_ORDER), code))
    return codes


def current_language() -> str:
    for bucket_name in ("browser", "user"):
        try:
            code = getattr(app.storage, bucket_name).get("lang")
        except Exception:
            continue
        if code in LANGUAGES:
            return code
    return DEFAULT_LANGUAGE if DEFAULT_LANGUAGE in LANGUAGES else (ordered_language_codes() or [DEFAULT_LANGUAGE])[0]


def text_direction(code: str | None = None) -> str:
    code = code or current_language()
    return LANGUAGES.get(code, {}).get("dir", "ltr")


def is_rtl(code: str | None = None) -> bool:
    return text_direction(code) == "rtl"


def t(key: str, **kwargs) -> str:
    """Look up key in the active language, then English, then the key itself."""
    lang = current_language()
    text = CATALOGS.get(lang, {}).get(key)
    if text is None:
        text = CATALOGS.get(DEFAULT_LANGUAGE, {}).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text


def _store_language(code: str) -> None:
    for bucket_name in ("browser", "user"):
        try:
            getattr(app.storage, bucket_name)["lang"] = code
        except Exception:
            continue


def _on_language_change(event) -> None:
    code = getattr(event, "value", None)
    if not code or code not in LANGUAGES or code == current_language():
        return
    _store_language(code)
    ui.navigate.reload()


def language_switcher():
    """Native-name language list. The control has a visible and spoken label."""
    label = t("common.language")
    select = ui.select(
        label=label,
        options={code: LANGUAGES[code]["native"] for code in ordered_language_codes()},
        value=current_language(),
        on_change=_on_language_change,
    ).props("dense outlined options-dense").classes("language-switcher")
    select.props(f'aria-label="{escape(label, quote=True)}"')
    return select


def prepare_page(title_key: str = "common.app_title") -> None:
    """Set html lang/dir and the document title for the active language."""
    lang = current_language()
    direction = text_direction(lang)
    title = t(title_key)
    ui.add_head_html(_DIRECTION_CSS, shared=True)
    ui.add_head_html(
        "<script>"
        f"document.documentElement.lang={json.dumps(lang)};"
        f"document.documentElement.dir={json.dumps(direction)};"
        f"document.title={json.dumps(title)};"
        "</script>"
    )

    def apply_document():
        ui.run_javascript(
            "document.documentElement.lang=" + json.dumps(lang) + ";"
            "document.documentElement.dir=" + json.dumps(direction) + ";"
            "document.title=" + json.dumps(title) + ";"
        )

    ui.timer(0.05, apply_document, once=True)


def heading(tag: str, classes: str, key: str, **kwargs) -> None:
    ui.html(f'<{tag} class="{classes}">{escape(t(key, **kwargs))}</{tag}>')


def back_button():
    icon = "arrow_forward" if is_rtl() else "arrow_back"
    ui.button(t("common.go_back"), on_click=ui.navigate.back, icon=icon).props("flat color=primary size=lg")


def dashboard_button():
    ui.button(t("common.go_dashboard"), on_click=lambda: ui.navigate.to("/dashboard")).props("flat color=primary size=lg")


def copyright_footer() -> None:
    with ui.column().classes("w-full bg-gray-100 py-12 border-t mt-auto"):
        ui.label(t("common.copyright")).classes("text-xs text-gray-500 text-center mx-auto")


def site_footer(video_url: str) -> None:
    with ui.column().classes("w-full bg-gray-100 py-36 mt-24 border-t"):
        with ui.column().classes("w-full max-w-4xl mx-auto gap-10 items-center text-center"):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "common.acknowledgements_title")
            ui.markdown(t("common.acknowledgements_body")).classes(
                "text-base leading-relaxed text-primary text-center mb-10"
            )
            heading("h3", "text-xl font-semibold mb-6 text-primary", "common.partners_title")
            with ui.grid(columns=2).classes("w-full gap-6 text-center"):
                ui.link(t("common.partner.ariel"), "https://www.ariel.ac.il/wp/en/").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.digital_pasts"), "https://digitalpasts.github.io/").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.heidelberg"), "https://www.uni-heidelberg.de/en").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.nfb"), "https://nfb.org/").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.rnib"), "https://www.rnib.org.uk/").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.envisionly"), "https://envisionly.tech/").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.liblouis"), "https://liblouis.io/").props("target=_blank").classes("text-accent hover:underline font-medium")
                ui.link(t("common.partner.nvda"), "https://www.nvaccess.org/").props("target=_blank").classes("text-accent hover:underline font-medium")
            with ui.row().classes("gap-16 mt-8"):
                with ui.column().classes("items-center"):
                    heading("h3", "text-xl font-semibold mb-3 text-primary", "common.documentation")
                    ui.link(t("common.user_guide"), "/documentation").classes("text-accent hover:underline font-medium")
                with ui.column().classes("items-center"):
                    heading("h3", "text-xl font-semibold mb-3 text-primary", "common.videos")
                    ui.link(t("common.video_link"), video_url).props("target=_blank").classes("text-accent hover:underline font-medium")
            ui.separator().classes("my-10 w-full")
            heading("h3", "text-xl font-semibold mb-4 text-primary", "common.contact")
            ui.label(t("common.contact_prompt")).classes("text-gray-600 mb-2")
            ui.link("info@nivlouie.com", "mailto:info@nivlouie.com").classes("text-accent hover:underline text-lg")
            ui.label(t("common.copyright")).classes("text-xs text-gray-500 mt-8")
