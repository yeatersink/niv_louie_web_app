# pages/06_edit_project_information.py

from nicegui import events, ui
from utils.storage import ensure_user_directories
from utils.project import project
from utils.project_utils import save_and_create_existing_csv
from utils.project_errors import show_project_error

# Add these missing imports so the regenerate functions are available
from utils.csv import regenerate_characters_using_hex, regenerate_hex_using_characters
from utils.braille import get_braille_from_text_in_source


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   # Reloads languages and project data
        print("LOG: User storage + project reloaded from edit_project_information page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


def save_project_edits(regenerate_characters, regenerate_hex, generate_braille, old_project_name):
    try:
        if regenerate_characters:
            regenerate_characters_using_hex()
        if regenerate_hex:
            regenerate_hex_using_characters()
        if generate_braille:
            get_braille_from_text_in_source()
        save_and_create_existing_csv(old_project_name)
    except KeyError as e:
        headers = list(project.project_text.columns) if project.project_text is not None else []
        show_project_error(
            "A mapped column is missing",
            f"Could not find one of the mapped columns ({e}). Headers in the file: " + ", ".join(f'"{c}"' for c in headers) + ".",
            "Your first row is the headers. One header has a space before Character. "
            "Re-save the CSV without leading spaces, or pick the header that JAWS reads with the space.",
        )
    except ValueError as e:
        show_project_error(
            "The project could not be saved",
            str(e),
            "Check that every list has a column from your file, then try Save project again.",
        )


@ui.page("/edit_project_information")
def edit_project_information():
    init_user_storage()
    regenerate_characters = False
    regenerate_hex = False
    generate_braille = False
    old_project_name = project.project_name

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):

        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back",
                     on_click=ui.navigate.back).props('flat color=primary size=lg')

            ui.button("Go to Dashboard",
                     on_click=lambda: ui.navigate.to("/dashboard")).props('flat color=primary size=lg')

        ui.html('<h1 class="text-3xl font-bold text-primary">Edit Project Information</h1>')

        if project.project_name is not None:
            project.set_all_fields()
            try:
                project.load_language_source()
            except Exception as ex:
                show_project_error(
                    "The project spreadsheet could not be read",
                    f"The saved CSV for this project could not be opened. {ex}",
                    "Upload a CSV whose first row is headers, or pick the header that JAWS reads with a leading space.",
                )

            with ui.card().classes('w-full p-8'):
                ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Basic Project Details</h2>')

                ui.input(label="What is the name of your project?",
                        value=project.project_name,
                        on_change=project.update_project_name).classes('w-full')

                ui.input(label="What is the language ISO code?",
                        value=project.project_language_code,
                        on_change=project.update_project_language_code).classes('w-full')

                ui.input(label="What is the language system?",
                        value=project.project_language_system_code,
                        on_change=project.update_project_language_system_code).classes('w-full')

        if project.project_text is not None:
            cols = [str(c).replace("\ufeff", "").strip() for c in project.project_text.columns]
            project.project_text.columns = cols

            def select_value(saved):
                if saved is None:
                    return None
                saved_name = str(saved).replace("\ufeff", "").strip()
                if saved_name in cols:
                    return saved_name
                return None

            with ui.card().classes('w-full p-8'):
                ui.html('<h2 class="text-2xl font-semibold mb-4 text-primary">Column matching</h2>')
                ui.label(
                    'Each list is a column from your uploaded CSV. Pick the column that matches what Niv Louie needs. Names must match the file, including spelling.'
                ).classes('mb-6 text-gray-700')

                ui.select(label="Character column (the glyph / print character)",
                         options=cols,
                         value=select_value(project.project_character_column),
                         on_change=project.update_project_character_column).classes('w-full')

                ui.select(label="Character name column",
                         options=cols,
                         value=select_value(project.project_name_column),
                         on_change=project.update_project_name_column).classes('w-full')

                ui.select(label="Unicode / Hex column",
                         options=cols,
                         value=select_value(project.project_unicode_column),
                         on_change=project.update_project_unicode_column).classes('w-full')

                ui.select(label="Type column",
                         options=cols,
                         value=select_value(project.project_type_column),
                         on_change=project.update_project_type_column).classes('w-full')

                ui.select(label="Braille column",
                         options=cols,
                         value=select_value(project.project_braille_column),
                         on_change=project.update_project_braille_column).classes('w-full')

            with ui.card().classes('w-full p-8'):
                ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Additional Information</h2>')

                ui.input(label="What are the language codes for the language for this project?",
                        value=project.project_supported_braille_languages,
                        on_change=project.update_project_supported_braille_languages).classes('w-full')

                ui.input(label="Please provide a brief explanation about the language in this project",
                        value=project.project_language_information,
                        on_change=project.update_project_language_information).classes('w-full')

                ui.input(label="Who are the contributors for this project?",
                        value=project.project_contributors,
                        on_change=project.update_project_contributors).classes('w-full')

                ui.input(label="What other braille tables would you like to include in this project?",
                        value=project.project_included_braille_tables,
                        on_change=project.update_project_included_braille_tables).classes('w-full')

                ui.input(label="Is this table intended to be a forward translation, a back translation, or both.",
                        value=project.project_test_display_type,
                        on_change=project.update_project_test_display_type).classes('w-full')

                ui.input(label="What characters or words do you want removed from your spreadsheet?",
                        value=project.project_replace,
                        on_change=project.update_project_replace).classes('w-full')

                # Regeneration options
                ui.html('<h3 class="text-xl font-semibold mt-8 mb-4 text-primary">Regeneration Options</h3>')

                def update_regenerate_characters(e: events.ValueChangeEventArguments):
                    nonlocal regenerate_characters
                    regenerate_characters = e.value

                ui.checkbox(text="Generate Characters using Unicode Column",
                           value=regenerate_characters,
                           on_change=update_regenerate_characters).classes('mb-3')

                def update_regenerate_hex(e: events.ValueChangeEventArguments):
                    nonlocal regenerate_hex
                    regenerate_hex = e.value

                ui.checkbox(text="Generate Unicode using Character Column",
                           value=regenerate_hex,
                           on_change=update_regenerate_hex).classes('mb-3')

                ui.checkbox(text="Generate Braille Characters for Braille Column",
                           value=generate_braille).classes('mb-3')

        ui.button("Save Changes",
                 on_click=lambda: save_project_edits(regenerate_characters, regenerate_hex, generate_braille, old_project_name)
        ).props('size=lg color=accent').classes('w-full mt-8')
