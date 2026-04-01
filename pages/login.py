# pages/login.py

from nicegui import app, ui
from utils.storage import create_new_user_session


def create_new_user_session_handler(nickname: str):
    if not nickname or not nickname.strip():
        ui.notify("Nickname is required", type='negative')
        return
    
    nickname = nickname.strip()
    
    try:
        # This safely creates the real user ID and private folders
        user_id = create_new_user_session(nickname)
        
        ui.notify(f"New private session created successfully for {nickname}", type='positive')
        ui.navigate.to('/login_information')
        
    except Exception as e:
        ui.notify(f"Error creating new session: {e}", type='negative')


def login_with_existing_id(user_id_input: str, remember_device: bool):
    if not user_id_input or len(user_id_input.strip()) < 10:
        ui.notify("Please enter a valid User ID", type='negative')
        return
    
    cleaned_id = user_id_input.strip()
    try:
        if hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user["user_id"] = cleaned_id
            
        if remember_device:
            ui.notify("✅ Successfully logged in and device remembered", type='positive')
        else:
            ui.notify("✅ Successfully logged in for this session", type='positive')
        
        ui.navigate.to('/dashboard')
    except Exception as e:
        ui.notify(f"Error logging in: {e}", type='negative')


@ui.page("/login")
def login():
    # Do NOT call ensure_user_directories() on the login page itself
    # It will be called only after successful login or new session creation

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
                     on_click=lambda: create_new_user_session_handler(nickname_input.value)
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