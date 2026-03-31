# pages/09_create_extention.py

from nicegui import ui
from utils.storage import ensure_user_directories, get_user_nvda_dir
from utils.project_extention import extention
from utils.project import project
from utils.nvda import create_nvda_extention


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()                    # Reloads languages for the project select
        extention.set_user_storage(get_user_nvda_dir())  # Fixed: pass the nvda directory
        print("LOG: User storage + project + extensions reloaded from create_extention page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/create_extention")
def create_extention():
    init_user_storage()

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):
        
        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back", 
                     on_click=ui.navigate.back).props('flat color=primary size=lg')
            
            ui.button("Home", 
                     on_click=lambda: ui.navigate.to("/")).props('flat color=primary size=lg')

            ui.html('<h1 class="text-3xl font-bold text-primary">Create NVDA Extension</h1>')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Extension Details</h2>')
            
            ui.input(
                label="What is the name of your Extension?",
                on_change=extention.update_extention_name
            ).classes('w-full mb-4')
            
            ui.input(
                label="Please briefly describe your Extension?",
                on_change=extention.update_extention_summary
            ).classes('w-full mb-4')
            
            ui.input(
                label="Please provide a more detailed description of your Extension?",
                on_change=extention.update_extention_description
            ).classes('w-full mb-4')
            
            ui.input(
                label="Who are the Authors of your Extension?",
                on_change=extention.update_extention_author
            ).classes('w-full mb-4')
            
            ui.input(
                label="Version number",
                on_change=extention.update_extention_version
            ).classes('w-full mb-4')
            
            ui.input(
                label="Minimum NVDA version supported",
                on_change=extention.update_extention_minimum_version
            ).classes('w-full mb-4')
            
            ui.input(
                label="Most recent NVDA version tested",
                on_change=extention.update_extention_last_tested_version
            ).classes('w-full mb-4')
            
            ui.input(
                label="Language / Locale this extension supports",
                on_change=extention.update_extention_locale
            ).classes('w-full mb-6')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Project Selection</h2>')
            
            ui.select(
                options=sorted(project.languages_list),
                label="What Projects do you want to include in this extension?",
                multiple=True,
                on_change=extention.update_extention_included_projects
            ).classes('w-full')

        # Main action button - teal accent for consistency
        def save_and_generate():
            extention.save_extention()           # Saves metadata first
            if extention.extention_name:         # Only generate if we have a valid name
                create_nvda_extention()          # Generates the .nvda-addon and triggers download

        ui.button("Save and Generate NVDA Add-on", 
                  on_click=save_and_generate, 
                  icon='save'
        ).props('size=lg color=accent').classes('w-full mt-8')

        # Cancel button
        ui.button("Cancel", 
                  on_click=lambda: ui.navigate.to('/nvda_extention_builder')
        ).props('flat color=primary').classes('mt-4')