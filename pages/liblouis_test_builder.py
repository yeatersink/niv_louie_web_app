# pages/12_liblouis_test_builder.py

from nicegui import events, ui
from utils.storage import ensure_user_directories
from utils.braille import create_braille_tests
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   
        print("LOG: User storage + project languages reloaded from liblouis_test_builder page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/liblouis_test_builder")
def liblouis_test_builder():
    init_user_storage()
    selected_projects = []

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8 items-center'):
        
        # Centered header - no Go Back button
        ui.html('<h1 class="text-3xl font-bold text-primary text-center">Lib Louis Test Builder</h1>')

        # Descriptive text as requested
        ui.html('''
            <p class="text-center text-gray-700 max-w-2xl">
                You can use your project to automatically generate a <strong>.yml</strong> file which is required 
                if you plan to publish a table with Liblouis.<br><br>
                This is also a great tool to test your own CSV / braille translation rules 
                to ensure that the CSV and braille table are producing the correct braille output.
            </p>
        ''').classes('mb-10')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Project Selection</h2>')
            
            def update_selected_project_list(e: events.ValueChangeEventArguments):
                nonlocal selected_projects
                selected_projects = e.value if e.value else []
                
                if selected_projects:
                    project.set_project_name(selected_projects[0])
                    project.set_all_fields()
                    print(f"DEBUG: Selected project '{selected_projects[0]}' | Language code set to '{project.project_language_code}'")
                    ui.notify(f"Selected project: {selected_projects[0]} (language code: {project.project_language_code})")

            ui.select(
                label="What projects do you want to generate a test from?", 
                options=sorted(project.languages_list), 
                multiple=True, 
                with_input=True, 
                on_change=update_selected_project_list
            ).classes('w-full')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Upload Test Document</h2>')
            
            ui.upload(
                label="What document do you want to generate a test from?", 
                on_upload=project.handle_test_upload, 
                auto_upload=True
            ).props('color=accent').classes('w-full')

        # Main action button
        ui.button(
            "Generate and download YAML Test for Lib Louis", 
            on_click=lambda: create_braille_tests(selected_projects)
        ).props('size=lg color=accent').classes('w-full mt-6')

        # Home button
        ui.button("Return to Home", 
                 on_click=lambda: ui.navigate.to("/")
        ).props('flat color=primary size=lg').classes('w-full mt-8')