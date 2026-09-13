# pages/05_project_information.py

from nicegui import ui
from utils.storage import ensure_user_directories
from utils.project import project
from utils.project_utils import save_and_create_csv


def init_user_storage():
    try:
        ensure_user_directories()
        print("LOG: User storage initialized from project_information page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/project_information")
def project_information():
    init_user_storage()

    if project.project_text is None:
        ui.notify("Upload a CSV first")
        ui.navigate.to("/create_project")
        return

    cols = [str(c).replace("\ufeff", "").strip() for c in project.project_text.columns]
    project.project_text.columns = cols

    def select_value(saved):
        if saved is None:
            return None
        saved_name = str(saved).replace("\ufeff", "").strip()
        if saved_name in cols:
            return saved_name
        return None

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):

        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back",
                     on_click=ui.navigate.back).props('flat color=primary size=lg')

            ui.button("Go to Dashboard",
                     on_click=lambda: ui.navigate.to("/dashboard")).props('flat color=primary size=lg')

        ui.html('<h1 class="text-3xl font-bold text-primary">Project information</h1>')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-primary">Liblouis metadata</h2>')
            ui.label('These fields become the metadata header of the Liblouis table.').classes('mb-6 text-gray-700')

            ui.input(label="What is the name of your project?",
                    value=project.project_name,
                    on_change=project.update_project_name).classes('w-full')

            ui.input(label="What is the language ISO code?",
                    value=project.project_language_code,
                    on_change=project.update_project_language_code).classes('w-full')

            ui.input(label="What is the language system?",
                    value=project.project_language_system_code,
                    on_change=project.update_project_language_system_code).classes('w-full')

            ui.input(label="What is the name you want to be displayed for your project?",
                    value=project.project_display_name,
                    on_change=project.update_project_display_name).classes('w-full')

            ui.input(label="What is the index name of your project?",
                    value=project.project_index_name,
                    on_change=project.update_project_index_name).classes('w-full')

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

        ui.button("Save Project",
                 on_click=save_and_create_csv
        ).props('size=lg color=primary').classes('w-full mt-8')
