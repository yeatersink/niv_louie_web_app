# pages/login_information.py

from nicegui import ui, app
from utils.storage import get_current_web_user_id, ensure_user_directories
from datetime import datetime


def download_login_info(user_id: str, nickname: str):
    """Generate and trigger download of login information as TXT file"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"Niv_Louie_Login_Info_{timestamp}.txt"
        
        content = f"""Niv Louie Login Information
================================

User ID: {user_id}
Nickname: {nickname}
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

IMPORTANT:
• Save this information in a safe place.
• You will need this User ID to log in from any device.
• If there is no activity for 6 months, the account will be automatically deleted.

Niv Louie - Free and Open Source (GPL-3.0)
© 2026 Niv Louie
"""

        ui.download(content.encode('utf-8'), filename=filename, media_type='text/plain')
        ui.notify("✅ Login information downloaded successfully to your Downloads folder", type='positive')
        
    except Exception as e:
        ui.notify(f"Download failed: {str(e)}", type='negative')


def copy_to_clipboard(user_id: str, nickname: str):
    """Copy login information to clipboard"""
    try:
        text = f"""Niv Louie Login Information

User ID: {user_id}
Nickname: {nickname}

Save this information safely. You will need the User ID to log in from any device."""

        ui.run_javascript(f'navigator.clipboard.writeText(`{text}`)')
        ui.notify("✅ Login information copied to clipboard", type='positive')
        
    except Exception as e:
        ui.notify(f"Copy failed: {str(e)}", type='negative')


def send_email_login_info(email: str, user_id: str, nickname: str):
    """Placeholder for email functionality"""
    if not email or '@' not in email:
        ui.notify("Please enter a valid email address", type='negative')
        return
    ui.notify(f"✅ Login information would be sent to {email} (email feature coming soon)", type='positive')


@ui.page("/login_information")
def login_information():
    ensure_user_directories()
    
    user_id = get_current_web_user_id()
    nickname = app.storage.user.get("nickname", "User")

    # Global layout styling
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    # Header
    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label('Niv Louie').classes('text-3xl font-bold tracking-tight')
            ui.space()
            ui.button('Log Out', 
                     on_click=lambda: ui.navigate.to('/')).props('flat color=white')

    # Main content
    with ui.column().classes('flex-1 w-full max-w-lg mx-auto p-8 gap-10 items-center'):

        ui.html('<h1 class="text-4xl font-bold text-center text-primary">Your private session is ready!</h1>')
        
        ui.label('Please save your login information before continuing to the dashboard.').classes('text-lg text-center text-gray-700')

        # Login info display card
        with ui.card().classes('p-8 w-full text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Your Login Details</h2>')
            
            with ui.column().classes('gap-4 text-left w-full'):
                ui.label(f"**User ID:**").classes('text-lg font-medium')
                ui.label(user_id).classes('font-mono bg-gray-100 p-4 rounded text-base break-all')
                
                ui.label(f"**Nickname:**").classes('text-lg font-medium mt-4')
                ui.label(nickname).classes('text-xl text-primary')

        ui.html('<h2 class="text-2xl font-semibold text-center text-primary mt-6">How would you like to save your login info?</h2>')

        # Option 1: Download - Now uses header + button (consistent with Email)
        with ui.card().classes('p-8 w-full'):
            ui.html('<h3 class="text-xl font-semibold mb-4">1. Download login information</h3>')
            ui.label('Saves a .txt file to your Downloads folder with your User ID and nickname').classes('text-gray-600 mb-6')
            
            ui.button('Download Login File', 
                     on_click=lambda: download_login_info(user_id, nickname)
            ).props('color=accent size=lg').classes('w-full')

        # Option 2: Email
        with ui.card().classes('p-8 w-full'):
            ui.html('<h3 class="text-xl font-semibold mb-4">2. Email it to myself</h3>')
            
            email_input = ui.input(
                label="Your email address",
                placeholder="you@example.com"
            ).classes('w-full').props('type=email')
            
            ui.button('Send Email', 
                     on_click=lambda: send_email_login_info(email_input.value, user_id, nickname)
            ).props('color=accent size=lg').classes('w-full mt-4')

        # Option 3: Copy to clipboard - kept as card for quick action
        with ui.card().classes('p-8 w-full cursor-pointer hover:bg-gray-50') as copy_card:
            with ui.row().classes('items-center gap-6 w-full'):
                ui.icon('content_copy', size='3xl', color='primary')
                with ui.column().classes('flex-1'):
                    ui.html('<h3 class="text-xl font-semibold">3. Copy to clipboard</h3>')
                    ui.label('Quick copy for pasting elsewhere').classes('text-gray-600')
            copy_card.on('click', lambda: copy_to_clipboard(user_id, nickname))

        # Continue button
        ui.button('Continue to My Dashboard', 
                 on_click=lambda: ui.navigate.to('/dashboard')
        ).props('color=primary size=lg').classes('w-full mt-10')

    # Footer
    with ui.column().classes('w-full bg-gray-100 py-12 border-t mt-auto'):
        ui.label('© 2026 Niv Louie - Free and Open Source (GPL-3.0)').classes('text-xs text-gray-500 text-center mx-auto')