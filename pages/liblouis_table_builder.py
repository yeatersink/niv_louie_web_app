# pages/11_liblouis_table_builder.py

from nicegui import ui
from utils.i18n import heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories
from utils.braille import create_braille_table
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   # This reloads project.languages_list for the select
        print("LOG: User storage + project languages reloaded from liblouis_table_builder page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/liblouis_table_builder")
def liblouis_table_builder():
    prepare_page("table.title")
    init_user_storage()

    with ui.column().classes('w-full max-w-2xl mx-auto p-8 gap-8 items-center'):
        with ui.row().classes('w-full justify-end'):
            language_switcher()
        
        heading("h1", "text-3xl font-bold text-primary text-center", "table.title")
        ui.label(t("table.intro")).classes('text-center text-gray-700 max-w-md mb-8')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "table.select")
            
            ui.select(
                label=t("table.which"), 
                options=sorted(project.languages_list), 
                with_input=True, 
                on_change=project.update_project_name
            ).classes('w-full')

        ui.button(t("table.generate"),
                 on_click=lambda: create_braille_table(include_metadata=True)
        ).props('size=lg color=accent').classes('w-full')

        ui.button(t("table.generate_plain"),
                 on_click=lambda: create_braille_table(include_metadata=False)
        ).props('size=lg color=accent').classes('w-full')

        ui.label(t("table.note")).classes('text-center text-gray-700')

        ui.button(t("common.return_dashboard"),
                 on_click=lambda: ui.navigate.to("/dashboard")
        ).props('flat color=primary size=lg').classes('w-full mt-8')