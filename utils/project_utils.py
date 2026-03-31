# utils/project_utils.py

from nicegui import app, events, ui
from utils.braille import create_braille_table, create_braille_tests, get_braille_from_text_in_source
from utils.csv import create_filtered_csv, regenerate_characters_using_hex, regenerate_hex_using_characters
from utils.nvda import add_characters_to_nvda, generate_locale_file, generate_character_set, create_nvda_extention
from utils.project import project
from utils.storage import ensure_user_directories


user_actions = []

actions = {
    "Add Characters to NVDA": {"action": add_characters_to_nvda, "notification": "Added characters to NVDA!"},
    "create extention for NVDA": {"action": create_nvda_extention, "notification": "Extention created for NVDA !"},
    "Write Table for Lib Louis": {"action": create_braille_table, "notification": "Table written for Lib Louis!"},
    "Write Test for Lib Louis": {"action": create_braille_tests, "notification": "Test written for Lib Louis!"}
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

def save_and_create_csv():
    ensure_user_directories()
    project.save_project()
    create_filtered_csv()

def save_and_create_existing_csv(old_project_name):
    ensure_user_directories()
    project.save_project()
    create_filtered_csv()
    # TODO: handle renaming if needed in future