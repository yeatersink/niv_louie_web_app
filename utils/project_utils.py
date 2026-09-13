# utils/project_utils.py

from nicegui import app, events, ui
from utils.braille import create_braille_table, create_braille_tests, get_braille_from_text_in_source
from utils.csv import create_filtered_csv, regenerate_characters_using_hex, regenerate_hex_using_characters
from utils.nvda import add_characters_to_nvda, generate_locale_file, generate_character_set, create_nvda_extention
from utils.project import project
from utils.storage import ensure_user_directories
from utils.project_errors import ProjectCsvError, show_project_error, format_header_list


user_actions = []

actions = {
    "Add Characters to NVDA": {"action": add_characters_to_nvda, "notification": "Added characters to NVDA!"},
    "create extention for NVDA": {"action": create_nvda_extention, "notification": "Extention created for NVDA !"},
    "Write Table for Liblouis": {"action": create_braille_table, "notification": "Table written for Liblouis!"},
    "Write Test for Liblouis": {"action": create_braille_tests, "notification": "Test written for Liblouis!"}
}

actions_name_list = list(actions.keys())

def perform_user_actions():
    ensure_user_directories()   # Ensure user folders exist before actions
    project.set_all_fields()
    global user_actions
    for action in user_actions:
        if action in actions:
            actions[action]["action"]()
            ui.notify(actions[action]["notification"])

def update_user_actions(e: events.ValueChangeEventArguments):
    global user_actions
    user_actions = e.value

def _headers_for_error():
    if project.project_text is None:
        return "(none)"
    return format_header_list(project.project_text.columns)

def _save_project_and_filter(replace_existing=False):
    ensure_user_directories()
    try:
        if not project.save_project(replace_existing=replace_existing):
            return
        create_filtered_csv()
    except ProjectCsvError as e:
        show_project_error(e.title, e.message, e.how_to_fix)
        return
    except KeyError as e:
        show_project_error(
            "A mapped column is missing",
            (
                f"Could not find one of the mapped columns ({e}). "
                f"Headers in the file: {_headers_for_error()}."
            ),
            "Your first row is the headers. One header has a space before Character. "
            "Re-save the CSV without leading spaces, or pick the header that JAWS reads with the space.",
        )
        return
    except ValueError as e:
        show_project_error(
            "The project could not be saved",
            str(e),
            "Check that every list has a column from your file, then try Save project again.",
        )
        return
    ui.notify("Your project is saved successfully.", type="positive")
    ui.navigate.to("/dashboard")

def save_and_create_csv():
    _save_project_and_filter(replace_existing=False)

def save_and_create_existing_csv(old_project_name):
    _save_project_and_filter(replace_existing=True)
    # TODO: handle renaming if needed in future
