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


@ui.page("/create_project")
def create_project():
    init_user_storage()

    with ui.column().classes('w-full max-w-2xl mx-auto p-8 gap-8 items-center'):
        
        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back", 
                     on_click=ui.navigate.back).props('flat color=primary size=lg')
            
            ui.html('<h1 class="text-3xl font-bold text-primary">Create New Project</h1>')

        ui.html('<h2 class="text-2xl font-semibold text-primary text-center">Upload your Spreadsheet</h2>')
        
        # Upload area in a clean card
        with ui.card().classes('w-full p-10 text-center'):
            ui.icon('upload_file', size='4rem').classes('text-primary mb-4')
            ui.label('Drop your CSV spreadsheet here or click to browse').classes('text-lg text-gray-600 mb-6')
            ui.upload(
                on_upload=project.handle_file_upload, 
                auto_upload=True,
                label='Select CSV File'
            ).props('color=accent').classes('w-full max-w-md mx-auto')   # Teal accent for upload

        # Continue button - teal accent for visual interest
        ui.button('Continue to Project Information', 
                  on_click=lambda: ui.navigate.to('/project_information')
        ).props('size=lg color=accent').classes('w-full max-w-md')

        ui.label('Supported: Unicode symbol, hex, name, braille columns').classes('text-sm text-gray-500')