# pages/04_create_project.py

from nicegui import ui
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
        ui.notify("Upload a CSV first")
        return
    ui.navigate.to("/project_information")


@ui.page("/create_project")
def create_project():
    init_user_storage()

    with ui.column().classes('w-full max-w-2xl mx-auto p-8 gap-8 items-center'):

        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back",
                     on_click=ui.navigate.back).props('flat color=primary size=lg')

            ui.button("Go to Dashboard",
                     on_click=lambda: ui.navigate.to("/dashboard")).props('flat color=primary size=lg')

        ui.html('<h1 class="text-3xl font-bold text-primary">Create a project</h1>')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-primary">How this works</h2>')
            ui.html('''
                <ol class="text-gray-700 space-y-2" style="list-style: decimal; padding-left: 1.5rem;">
                    <li>Upload your spreadsheet. Use Choose file and pick a .csv from this computer.</li>
                    <li>Continue to project information. You will enter names and codes used as Liblouis table metadata.</li>
                    <li>Match each combo box to a column in your file, then Save project.</li>
                </ol>
            ''')

        with ui.card().classes('w-full p-10 text-center'):
            ui.icon('upload_file', size='4rem').classes('text-primary mb-4')
            ui.upload(
                on_upload=project.handle_file_upload,
                auto_upload=True,
                label='Choose file'
            ).props('color=accent accept=.csv').classes('w-full max-w-md mx-auto')
            ui.label('CSV only. First row must be headers.').classes('text-sm text-gray-600 mt-4')

        ui.button('Continue to project information',
                  on_click=continue_to_project_information
        ).props('size=lg color=accent').classes('w-full max-w-md')
