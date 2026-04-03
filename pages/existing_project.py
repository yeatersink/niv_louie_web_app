# pages/03_existing_project.py

from nicegui import events, ui
from utils.storage import ensure_user_directories
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()          # reloads the correct user data
        print("LOG: User storage + project languages reloaded from existing_project page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/existing_project")
def existing_project():
    init_user_storage()

    with ui.column().classes('w-full max-w-2xl mx-auto p-8 gap-8 items-center'):
        
        # Centered main header 
        ui.html('<h1 class="text-3xl font-bold text-primary text-center">Project Dashboard</h1>')

        # New description text as requested
        ui.html('''
            <p class="text-center text-gray-700 max-w-md">
                This is your project management dashboard. 
                Here you will upload, edit, and create your projects 
                that will be used throughout the rest of the application.
            </p>
        ''').classes('mb-6')

        ui.html('<h2 class="text-2xl font-semibold text-primary text-center">Welcome to your project dashboard.</h2>')

        # Main action buttons
        with ui.row().classes('gap-4 w-full justify-center'):
            ui.button("Create a New Project", 
                     on_click=lambda: ui.navigate.to("/create_project")
            ).props('size=lg color=accent').classes('flex-1 max-w-xs')

            ui.button("Edit Selected Project", 
                     on_click=lambda: ui.navigate.to("/edit_project_information")
            ).props('size=lg color=accent').classes('flex-1 max-w-xs')

        # Project selection card
        with ui.card().classes('w-full p-8'):
            ui.html('<h3 class="text-xl font-semibold mb-6 text-primary">Select an Existing Project</h3>')
            
            language_select = ui.select(
                options=sorted(project.languages_list),
                label="Choose Project",
                with_input=True,
                on_change=project.update_project_name
            ).classes('w-full')
            
            # Force the dropdown to refresh after reload
            ui.timer(0.1, lambda: setattr(language_select, 'options', sorted(project.languages_list)), once=True)

        # Danger zone card for deletion
        with ui.card().classes('w-full p-8 bg-red-50 border border-red-200'):
            ui.html('<h3 class="text-xl font-semibold mb-4 text-primary">Danger Zone</h3>')
            ui.label('Permanently remove the currently selected project. This action cannot be undone.').classes('text-gray-600 mb-6')
            
            with ui.dialog() as dialog, ui.card().classes('p-8 w-full max-w-md'):
                ui.html('<h3 class="text-2xl font-bold text-negative mb-6 text-center">Are you sure?</h3>')
                ui.label('You are about to permanently delete this project and all its associated files.').classes('text-center mb-8')
                
                with ui.row().classes('gap-4 w-full justify-center'):
                    ui.button("Cancel", on_click=dialog.close).props('flat color=primary size=lg')
                    def confirm_delete():
                        project.remove_project()
                        # Refresh list immediately after delete
                        language_select.options = sorted(project.languages_list)
                        dialog.close()
                        ui.notify("Project has been permanently deleted", type='negative')
                    ui.button("Yes, Delete Project", on_click=confirm_delete).props('color=negative size=lg')

            ui.button("Remove Project", 
                     on_click=dialog.open
            ).props('color=negative size=lg').classes('w-full')

        # Updated button - changed only text and destination as requested
        ui.button("Return to Dashboard", 
                 on_click=lambda: ui.navigate.to("/dashboard")
        ).props('flat color=primary size=lg').classes('w-full mt-4')