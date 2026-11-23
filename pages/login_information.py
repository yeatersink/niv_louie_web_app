# pages/login_information.py

import json
from nicegui import ui, app
from utils.i18n import copyright_footer, heading, language_switcher, prepare_page, t
from utils.storage import get_current_web_user_id, ensure_user_directories
from utils.email import send_login_email   # ← New import
from datetime import datetime


def download_login_info(user_id: str, nickname: str):
    """Generate and trigger download of login information as TXT file"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"Niv_Louie_Login_Info_{timestamp}.txt"
        
        content = t(
            "login_info.file_body",
            user_id=user_id,
            nickname=nickname,
            created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        ui.download(content.encode('utf-8'), filename=filename, media_type='text/plain')
        ui.notify(t("login_info.downloaded"), type='positive')
        
    except Exception as e:
        ui.notify(t("login_info.download_failed", error=e), type='negative')


def copy_to_clipboard(user_id: str, nickname: str):
    """Copy login information to clipboard"""
    try:
        text = t("login_info.copy_body", user_id=user_id, nickname=nickname)
        ui.run_javascript(f"navigator.clipboard.writeText({json.dumps(text)})")
        ui.notify(t("login_info.copied"), type='positive')
        
    except Exception as e:
        ui.notify(t("login_info.copy_failed", error=e), type='negative')


def send_email_login_info(email: str, user_id: str, nickname: str):
    """Send login information via email using real SMTP"""
    if not email or '@' not in email:
        ui.notify(t("login_info.invalid_email"), type='negative')
        return
    
    # Call the real email function from utils/email.py
    success = send_login_email(to_email=email, user_id=user_id, nickname=nickname)
    
    if success:
        ui.notify(t("login_info.sent", email=email), type='positive')
    else:
        ui.notify(t("login_info.send_failed"), type='negative')


@ui.page("/login_information")
def login_information():
    prepare_page("login_info.title")
    ensure_user_directories()
    
    user_id = get_current_web_user_id()
    nickname = app.storage.user.get("nickname", "User")

    # Global layout styling
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    # Header
    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label(t("common.brand")).classes('text-3xl font-bold tracking-tight')
            ui.space()
            language_switcher()
            ui.button(t("common.log_out"), 
                     on_click=lambda: ui.navigate.to('/')).props('flat color=white')

    # Main content
    with ui.column().classes('flex-1 w-full max-w-lg mx-auto p-8 gap-10 items-center'):

        heading("h1", "text-4xl font-bold text-center text-primary", "login_info.title")
        
        ui.label(t("login_info.save_prompt")).classes('text-lg text-center text-gray-700')

        # Login info display card
        with ui.card().classes('p-8 w-full text-center'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "login_info.details")
            
            with ui.column().classes('gap-4 text-left w-full'):
                ui.label(t("login_info.user_id_label")).classes('text-lg font-medium')
                ui.label(user_id).classes('font-mono bg-gray-100 p-4 rounded text-base break-all')
                
                ui.label(t("login_info.nickname_label")).classes('text-lg font-medium mt-4')
                ui.label(nickname).classes('text-xl text-primary')

        heading("h2", "text-2xl font-semibold text-center text-primary mt-6", "login_info.how_save")

        # Option 1: Download
        with ui.card().classes('p-8 w-full'):
            heading("h3", "text-xl font-semibold mb-4", "login_info.download_title")
            ui.label(t("login_info.download_help")).classes('text-gray-600 mb-6')
            
            ui.button(t("login_info.download_button"), 
                     on_click=lambda: download_login_info(user_id, nickname)
            ).props('color=accent size=lg').classes('w-full')

        # Option 2: Email - Now using real sending
        with ui.card().classes('p-8 w-full'):
            heading("h3", "text-xl font-semibold mb-4", "login_info.email_title")
            
            email_input = ui.input(
                label=t("login_info.email_label"),
                placeholder=t("login_info.email_placeholder")
            ).classes('w-full').props('type=email')
            
            ui.button(t("login_info.send"), 
                     on_click=lambda: send_email_login_info(email_input.value, user_id, nickname)
            ).props('color=accent size=lg').classes('w-full mt-4')

        # Option 3: Copy to clipboard
        with ui.card().classes('p-8 w-full cursor-pointer hover:bg-gray-50') as copy_card:
            with ui.row().classes('items-center gap-6 w-full'):
                ui.icon('content_copy', size='3xl', color='primary')
                with ui.column().classes('flex-1'):
                    heading("h3", "text-xl font-semibold", "login_info.copy_title")
                    ui.label(t("login_info.copy_help")).classes('text-gray-600')
            copy_card.on('click', lambda: copy_to_clipboard(user_id, nickname))

        # Continue button
        ui.button(t("login_info.continue"), 
                 on_click=lambda: ui.navigate.to('/dashboard')
        ).props('color=primary size=lg').classes('w-full mt-10')

    copyright_footer()