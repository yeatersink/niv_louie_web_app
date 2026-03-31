# gui.py - Web version of Niv Louie
# Clean version with reliable storage calls on every page

from nicegui import app, events, ui
from utils.project import project
from utils.project_extention import extention
from utils.project_utils import save_and_create_csv, save_and_create_existing_csv
from utils.braille_document_manager import document
from utils.braille import create_braille_table, create_braille_tests, get_braille_from_text_in_source
from utils.csv import create_filtered_csv, regenerate_characters_using_hex, regenerate_hex_using_characters
from utils.nvda import create_nvda_extention
from utils.storage import get_private_user_dir, get_user_projects_dir, ensure_user_directories
from pathlib import Path
import os


def get_current_user_info():
    try:
        from utils.storage import get_current_web_user_id
        user_id = get_current_web_user_id()
        private_dir = get_private_user_dir()
        projects_dir = get_user_projects_dir()
        return user_id, str(private_dir), str(projects_dir)
    except Exception as e:
        print(f"LOG: Error getting user info: {e}")
        return "initializing...", "waiting...", "waiting..."


def init_user_storage():
    try:
        ensure_user_directories()
        user_id, private_dir, projects_dir = get_current_user_info()
        
        # Connect storage to project object
        project.set_user_storage(projects_dir)
        
        print(f"LOG: User storage initialized for folder: {projects_dir}")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


# ====================== HOME PAGE ======================
@ui.page("/")
def home():
    init_user_storage()
    user_id, private_path, projects_path = get_current_user_info()

    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label('Niv Louie').classes('text-3xl font-bold tracking-tight')
            ui.space()
            ui.button('Log In', on_click=lambda: ui.navigate.to('/login')).props('flat color=white')
            ui.button('Collaborate', on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    with ui.column().classes('w-full max-w-4xl mx-auto p-8 gap-12 items-center'):
        ui.html('<h1 class="text-4xl font-bold text-center">Welcome to Niv Louie</h1>')

        with ui.card().classes('p-6 w-full max-w-3xl bg-green-50'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center">Current Session</h2>')
            ui.label(f'User ID: {user_id}').classes('font-mono text-lg text-center')
            ui.label(f'Private folder: {private_path}').classes('text-sm text-gray-600 text-center')
            ui.label(f'Projects saved to: {projects_path}').classes('text-sm text-gray-600 text-center')

        with ui.card().classes('p-8 w-full max-w-3xl'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center">What Niv Louie Can Do</h2>')
            ui.markdown('''
Niv Louie allows anyone to upload simple CSV files containing Unicode symbols, character names, and desired Braille representations, then instantly generates:

1. **Lib Louis Braille tables** for high-quality Braille translation  
2. **Custom Braille** for development of new Braille scripts and systems for any language or writing system, even those without existing Braille support  
3. **Braille documents** that can be printed or embossed from the custom tables built with Niv Louie  
4. **NVDA extensions** that give screen readers immediate spoken and Braille access to any Unicode character or symbol in digital content, including math, music, scientific symbols, emojis, and more.
            ''').classes('text-base leading-relaxed')

        # Tool cards (shortened for clarity - keep your full cards if you prefer)
        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.button('Go to Project Manager', on_click=lambda: ui.navigate.to('/existing_project')).props('size=lg').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.button('Go to Braille Document Builder', on_click=lambda: ui.navigate.to('/braille_document_builder')).props('size=lg').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.button('Go to NVDA Extension Builder', on_click=lambda: ui.navigate.to('/nvda_extention_builder')).props('size=lg').classes('w-full')

    with ui.footer().classes('bg-gray-100 py-8 mt-12'):
        ui.label('Making the World Accessible, One Braille Table at a Time').classes('text-center text-gray-600')


# ====================== LOGIN PAGE ======================
@ui.page("/login")
def login():
    ui.button("← Go Back", on_click=ui.navigate.back).props('flat')

    with ui.column().classes('w-full max-w-lg mx-auto p-8 gap-10 items-center'):
        ui.html('<h1 class="text-4xl font-bold text-center">Welcome to Niv Louie</h1>')
        
        with ui.card().classes('p-8 w-full'):
            ui.button('Log in as New User', on_click=create_new_user_session).props('color=primary size=lg').classes('w-full')

        with ui.card().classes('p-8 w-full'):
            user_id_input = ui.input(label="Your User ID").classes('w-full')
            remember = ui.checkbox("Remember this device", value=True)
            ui.button('Log In with Existing User ID', 
                     on_click=lambda: login_with_existing_id(user_id_input.value, remember.value)
            ).props('color=positive size=lg').classes('w-full')


def create_new_user_session():
    try:
        from utils.storage import get_current_web_user_id
        new_id = get_current_web_user_id()
        app.storage.user["user_id"] = new_id
        init_user_storage()

        with ui.dialog() as dialog, ui.card().classes('p-10 w-full max-w-lg'):
            ui.label('New Private Session Created').classes('text-3xl font-bold text-center')
            ui.markdown(f'**Your User ID:**\n\n`{new_id}`').classes('font-mono text-lg bg-gray-100 p-6 rounded my-8 text-center')
            ui.label('Note: Inactive accounts (6 months) will be automatically deleted.').classes('text-sm text-gray-600 text-center')
            ui.button('Close', on_click=dialog.close).props('flat')
        dialog.open()
        ui.navigate.to('/')
    except Exception as e:
        ui.notify(f"Error: {e}", type='negative')


def login_with_existing_id(user_id: str, remember: bool):
    if not user_id or len(user_id.strip()) < 10:
        ui.notify("Please enter a valid User ID", type='negative')
        return
    cleaned = user_id.strip()
    app.storage.user["user_id"] = cleaned
    init_user_storage()
    ui.notify("Logged in successfully", type='positive')
    ui.navigate.to('/')


# ====================== Other pages (minimal for now) ======================
@ui.page("/existing_project")
def existing_project():
    init_user_storage()
    ui.button("Go Back", on_click=ui.navigate.back)
    ui.label("Project Manager")
    ui.button("Create New Project", on_click=lambda: ui.navigate.to("/create_project"))
    ui.button("Home", on_click=lambda: ui.navigate.to("/"))


@ui.page("/create_project")
def create_project():
    init_user_storage()
    ui.button("Go Back", on_click=ui.navigate.back)
    ui.upload(on_upload=project.handle_file_upload, auto_upload=True)


# Add the rest of your pages (braille_document_builder, nvda_extention_builder, etc.) as before.
# For now, keep them as they were in your previous gui.py.

# ====================== WEB SERVER SETUP ======================
ui.run(
    host="0.0.0.0",
    port=8080,
    title="Niv Louie... Making the World Accessible, One Braille Table at a Time",
    reload=False,
    show=True,
    storage_secret="niv_louie_secret_key_2026"
)