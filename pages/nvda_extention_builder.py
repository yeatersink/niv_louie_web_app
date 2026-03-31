# pages/08_nvda_extention_builder.py

from nicegui import ui
from utils.storage import ensure_user_directories, get_user_nvda_dir
from utils.project_extention import extention
from utils.nvda import create_nvda_extention


def init_user_storage():
    try:
        ensure_user_directories()
        extention.set_user_storage(get_user_nvda_dir())
        print("LOG: User storage + extensions reloaded from nvda_extention_builder page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/nvda_extention_builder")
def nvda_extention_builder():
    init_user_storage()

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8 items-center'):
        
        # Centered header
        ui.html('<h1 class="text-3xl font-bold text-primary text-center">NVDA Extension Builder</h1>')

        # Descriptive text
        ui.html('''
            <p class="text-center text-gray-700 max-w-2xl">
                Here you can use several different projects to build your own custom NVDA Add-on extension.<br>
                This allows you to combine multiple language tables, symbol sets, and custom braille rules into a single screen reader extension.
            </p>
        ''').classes('mb-10')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">How to Use This Tool</h2>')
            ui.html('''
                <p>This tool helps you create and manage NVDA screen reader extensions for your custom languages and symbol sets.</p>
                <p><strong>Tip:</strong> You can create one NVDA Add-on that includes <strong>multiple projects</strong>. 
                   This is especially useful for languages with many components, writing systems with lots of symbols, 
                   emojis, science notation, or chemistry symbols.</p>
            ''').classes('prose text-gray-700')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Your Saved Extensions</h2>')
            
            ui.select(
                label="Select an Extension", 
                options=sorted(extention.extentions_list), 
                on_change=extention.update_extention_name
            ).classes('w-full')

        # Uniform action buttons - all same size and style
        with ui.row().classes('gap-4 w-full flex-wrap justify-center'):
            ui.button("Create New Extension", 
                      on_click=lambda: ui.navigate.to("/create_extention"),
                      icon='add').props('size=lg color=accent').classes('min-w-[220px]')

            ui.button("Edit Selected Extension", 
                      on_click=lambda: ui.navigate.to("/edit_extention"),
                      icon='edit').props('size=lg color=accent').classes('min-w-[220px]')

            ui.button("Generate Selected Extension", 
                      on_click=create_nvda_extention,
                      icon='download').props('size=lg color=accent').classes('min-w-[220px]')

            ui.button("Download Selected Extension", 
                      on_click=lambda: download_extension(),
                      icon='file_download').props('size=lg color=accent').classes('min-w-[220px]')

        # Manage / Delete section
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Manage Extension</h2>')
            
            with ui.dialog() as dialog, ui.card().classes('p-8 w-full max-w-md'):
                ui.html('<h3 class="text-2xl font-bold text-negative mb-6 text-center">Delete Extension</h3>')
                ui.label("Are you sure you want to permanently remove this extension?").classes('text-center mb-8')
                
                with ui.row().classes('gap-4 w-full justify-center'):
                    ui.button("Cancel", on_click=dialog.close).props('flat color=primary size=lg')
                    def confirm_delete():
                        extention.remove_extention()
                        dialog.close()
                    ui.button("Yes, Delete", on_click=confirm_delete).props('color=negative size=lg')

            ui.button("Remove Selected Extension", 
                      on_click=dialog.open, 
                      icon='delete').props('color=negative size=lg').classes('w-full')

        # Home button
        ui.button("Return to Home", 
                 on_click=lambda: ui.navigate.to("/")
        ).props('flat color=primary size=lg').classes('w-full mt-6')


# Define download function
def download_extension():
    if not extention.extention_name:
        ui.notify("No extension selected", type="negative")
        return
    
    nvda_dir = get_user_nvda_dir()
    final_name = f"{extention.extention_name}.nvda-addon"
    file_path = nvda_dir / final_name
    
    try:
        all_files = [f.name for f in nvda_dir.iterdir() if f.is_file()]
        print(f"DEBUG: Files in nvda_extensions folder: {all_files}")
        print(f"DEBUG: Looking for: {final_name}")
    except Exception as list_err:
        print(f"DEBUG: Error listing files: {list_err}")
    
    if not file_path.exists():
        ui.notify(f"File not found: {final_name}", type="negative")
        ui.notify(f"Check folder: {nvda_dir}", type="warning")
        print(f"DEBUG: File does not exist at {file_path}")
        return
    
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        ui.notify(f"Downloading: {final_name}", type="positive")
        ui.download.content(
            file_content,
            filename=final_name,
            media_type="application/zip"
        )
        print(f"DEBUG: Manual download triggered for {file_path}")
    except Exception as e:
        ui.notify(f"Download error: {str(e)}", type="negative")
        print(f"DEBUG: Manual download exception: {e}")