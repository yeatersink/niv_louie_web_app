# pages/02_login.py

from nicegui import app, ui
from utils.storage import ensure_user_directories, get_current_web_user_id


def init_user_storage():
    try:
        ensure_user_directories()
        print("LOG: User storage initialized from login page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


def create_new_user_session(nickname: str):
    if not nickname or not nickname.strip():
        ui.notify("Nickname is required", type='negative')
        return
    
    nickname = nickname.strip()
    
    try:
        new_id = get_current_web_user_id()
        
        app.storage.user["user_id"] = new_id
        app.storage.user["nickname"] = nickname
        
        init_user_storage()

        with ui.dialog() as dialog, ui.card().classes('p-10 w-full max-w-lg'):
            ui.icon('check_circle', color='positive', size='3xl').classes('mx-auto')
            ui.html('<h2 class="text-3xl font-bold text-primary text-center mt-4">New Private Session Created</h2>')
            ui.markdown(f'**Your User ID is:**\n\n`{new_id}`').classes('text-center my-8 font-mono text-lg bg-gray-100 p-6 rounded')
            ui.label(f'**Nickname:** {nickname}').classes('text-center text-lg text-primary')
            ui.label('Note: If there is no activity for 6 months, the account will be automatically deleted.').classes('text-sm text-gray-600 text-center mt-6')
            
            with ui.row().classes('gap-4 w-full justify-center mt-8'):
                ui.button('Copy User ID', 
                         on_click=lambda: ui.notify('User ID copied!', type='positive')
                ).props('color=primary')
                ui.button('Close', on_click=dialog.close).props('flat color=primary')
        dialog.open()
        ui.navigate.to('/dashboard')   # Changed: go to dashboard after successful login
    except Exception as e:
        ui.notify(f"Error creating new session: {e}", type='negative')


def login_with_existing_id(user_id: str, remember_device: bool):
    if not user_id or len(user_id.strip()) < 10:
        ui.notify("Please enter a valid User ID", type='negative')
        return
    
    cleaned_id = user_id.strip()
    try:
        app.storage.user["user_id"] = cleaned_id
        if remember_device:
            ui.notify("✅ Successfully logged in and device remembered", type='positive')
        else:
            ui.notify("✅ Successfully logged in for this session", type='positive')
        init_user_storage()
        ui.navigate.to('/dashboard')   # Changed: go to dashboard after successful login
    except Exception as e:
        ui.notify(f"Error logging in: {e}", type='negative')


@ui.page("/login")
def login():
    init_user_storage()

    with ui.column().classes('w-full max-w-lg mx-auto p-8 gap-10'):
        
        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back", 
                     on_click=ui.navigate.back).props('flat color=primary size=lg')
            
            ui.html('<h1 class="text-4xl font-bold text-primary text-center">Welcome to Niv Louie</h1>')

        ui.label('Please choose how you would like to access your private workspace:').classes('text-lg text-center text-gray-700')

        # New User Card
        with ui.card().classes('p-8 w-full'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center text-primary">New User</h2>')
            ui.label('Create a new private session.').classes('text-center mb-6 text-gray-600')
            
            nickname_input = ui.input(label="Choose a Nickname", 
                                     placeholder="e.g. Matt, Teacher Sarah").classes('w-full mb-6')
            
            ui.button('Create New User Session', 
                     on_click=lambda: create_new_user_session(nickname_input.value)
            ).props('color=accent size=lg').classes('w-full')   

        # Existing User Card
        with ui.card().classes('p-8 w-full'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center text-primary">Existing User</h2>')
            ui.label('Log in with your existing User ID.').classes('text-center mb-6 text-gray-600')
            
            user_id_input = ui.input(label="Your User ID", 
                                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").classes('w-full')
            
            remember_checkbox = ui.checkbox("Remember this device", value=True).classes('w-full mt-4')

            ui.button('Log In with Existing User ID', 
                     on_click=lambda: login_with_existing_id(user_id_input.value, remember_checkbox.value)
            ).props('color=accent size=lg').classes('w-full mt-6')   