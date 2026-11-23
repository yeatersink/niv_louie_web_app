# pages/login.py

from nicegui import app, ui
from utils.i18n import back_button, heading, language_switcher, prepare_page, t
from utils.storage import create_new_user_session


def create_new_user_session_handler(nickname: str):
    if not nickname or not nickname.strip():
        ui.notify(t("login.nickname_required"), type='negative')
        return
    
    nickname = nickname.strip()
    
    try:
        # This safely creates the real user ID and private folders
        user_id = create_new_user_session(nickname)
        
        ui.notify(t("login.session_created", nickname=nickname), type='positive')
        ui.navigate.to('/login_information')
        
    except Exception as e:
        ui.notify(t("login.session_error", error=e), type='negative')


def login_with_existing_id(user_id_input: str, remember_device: bool):
    if not user_id_input or len(user_id_input.strip()) < 10:
        ui.notify(t("login.invalid_id"), type='negative')
        return
    
    cleaned_id = user_id_input.strip()
    try:
        if hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user["user_id"] = cleaned_id
            
        if remember_device:
            ui.notify(t("login.remembered"), type='positive')
        else:
            ui.notify(t("login.session_only"), type='positive')
        
        ui.navigate.to('/dashboard')
    except Exception as e:
        ui.notify(t("login.error", error=e), type='negative')


@ui.page("/login")
def login():
    # Do NOT call ensure_user_directories() on the login page itself
    # It will be called only after successful login or new session creation
    prepare_page("login.title")

    with ui.column().classes('w-full max-w-lg mx-auto p-8 gap-10'):
        
        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            back_button()
            language_switcher()
            
            heading("h1", "text-4xl font-bold text-primary text-center", "login.welcome")

        ui.label(t("login.choose")).classes('text-lg text-center text-gray-700')

        # New User Card
        with ui.card().classes('p-8 w-full'):
            heading("h2", "text-2xl font-semibold mb-4 text-center text-primary", "login.new_user")
            ui.label(t("login.new_user_help")).classes('text-center mb-6 text-gray-600')
            
            nickname_input = ui.input(label=t("login.nickname"), 
                                     placeholder=t("login.nickname_placeholder")).classes('w-full mb-6')
            
            ui.button(t("login.create"), 
                     on_click=lambda: create_new_user_session_handler(nickname_input.value)
            ).props('color=accent size=lg').classes('w-full')   

        # Existing User Card
        with ui.card().classes('p-8 w-full'):
            heading("h2", "text-2xl font-semibold mb-4 text-center text-primary", "login.existing")
            ui.label(t("login.existing_help")).classes('text-center mb-6 text-gray-600')
            
            user_id_input = ui.input(label=t("login.user_id"), 
                                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").classes('w-full font-mono')
            
            remember_checkbox = ui.checkbox(t("login.remember"), value=True).classes('w-full mt-4')

            ui.button(t("login.submit_existing"), 
                     on_click=lambda: login_with_existing_id(user_id_input.value, remember_checkbox.value)
            ).props('color=accent size=lg').classes('w-full mt-6')   