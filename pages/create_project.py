# pages/04_create_project.py

from html import escape
from nicegui import ui
from utils.i18n import back_button, dashboard_button, heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   # Ensures correct user folder and reloads languages
        print("LOG: User storage + project reloaded from create_project page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


def continue_to_project_information():
    if project.project_text is None:
        ui.notify(t("project.upload_csv_first"))
        return
    ui.navigate.to("/project_information")


@ui.page("/create_project")
def create_project():
    prepare_page("create.title")
    init_user_storage()

    with ui.column().classes('w-full max-w-2xl mx-auto p-8 gap-8 items-center'):

        with ui.row().classes('w-full items-center justify-between'):
            back_button()
            language_switcher()
            dashboard_button()

        heading("h1", "text-3xl font-bold text-primary", "create.title")

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-4 text-primary", "create.how_title")
            ui.html(
                '<ol class="text-gray-700 space-y-2" style="list-style: decimal; padding-inline-start: 1.5rem;">'
                f"<li>{escape(t('create.step1'))}</li>"
                f"<li>{escape(t('create.step2'))}</li>"
                f"<li>{escape(t('create.step3'))}</li>"
                "</ol>"
            )

        with ui.card().classes('w-full p-10 text-center'):
            ui.icon('upload_file', size='4rem').classes('text-primary mb-4')
            ui.upload(
                on_upload=project.handle_file_upload,
                auto_upload=True,
                label=t("create.choose_file")
            ).props('color=accent accept=.csv').classes('w-full max-w-md mx-auto')
            ui.label(t("create.csv_only")).classes('text-sm text-gray-600 mt-4')

        ui.button(t("create.continue"),
                  on_click=continue_to_project_information
        ).props('size=lg color=accent').classes('w-full max-w-md')
