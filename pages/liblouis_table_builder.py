# pages/11_liblouis_table_builder.py

from nicegui import ui
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
    init_user_storage()

    with ui.column().classes('w-full max-w-2xl mx-auto p-8 gap-8 items-center'):
        
        # Centered header - no Go Back button
        ui.html('<h1 class="text-3xl font-bold text-primary text-center">Lib Louis Table Builder</h1>')

        # Descriptive text as requested
        ui.html('''
            <p class="text-center text-gray-700 max-w-md">
                You can use your project to automatically create and download 
                a table ready to publish on Liblouis.
            </p>
        ''').classes('mb-8')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Select Project</h2>')
            
            ui.select(
                label="What project do you want to use?", 
                options=sorted(project.languages_list), 
                with_input=True, 
                on_change=project.update_project_name
            ).classes('w-full')

        # Main action button
        ui.button("Generate and Download table for Lib Louis", 
                 on_click=create_braille_table
        ).props('size=lg color=accent').classes('w-full')

        # Updated button - changed only text and destination as requested
        ui.button("Return to Dashboard", 
                 on_click=lambda: ui.navigate.to("/dashboard")
        ).props('flat color=primary size=lg').classes('w-full mt-8')