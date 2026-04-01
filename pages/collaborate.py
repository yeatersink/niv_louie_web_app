# pages/13_collaborate.py

from nicegui import ui, app
from utils.storage import generate_sync_code, claim_sync_code


@ui.page("/collaborate")
def collaborate():
    # Check if user is logged in
    user_id = app.storage.user.get("user_id") if hasattr(app.storage, 'user') and app.storage.user is not None else None

    if not user_id:
        with ui.column().classes('w-full max-w-md mx-auto p-8 text-center'):
            ui.icon('login', size='5xl', color='primary').classes('mx-auto mb-6')
            ui.html('<h1 class="text-3xl font-bold text-primary mb-4">Please Log In First</h1>')
            ui.label('You need to be logged in to use Sync Codes for collaboration.').classes('text-lg mb-8')
            ui.button('Go to Login', 
                     on_click=lambda: ui.navigate.to('/login')).props('size=lg color=accent')
        return

    # Global layout styling - consistent with other pages
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-10'):

        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back", 
                     on_click=ui.navigate.back).props('flat color=primary size=lg')
            
            ui.html('<h1 class="text-3xl font-bold text-primary">Collaborate with Others</h1>')

        ui.markdown("""
This page allows you to share your Niv Louie projects with others using a **Sync Code** 
and access projects shared with you from any device.
        """).classes('text-base leading-relaxed')

        # ==================== SECTION 1: Generate Sync Code ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">1. Generate Sync Code</h2>')
            ui.markdown("""
**Use this code on another device** (phone, tablet, laptop) to access all your projects and files.
The code is temporary and easy to read.
            """)

            sync_code_display = ui.label("Click the button below to generate your sync code").classes('text-lg font-medium text-center py-6')

            def generate_new_sync_code():
                try:
                    code = generate_sync_code()
                    sync_code_display.text = f"Your Sync Code:\n\n{code}"
                    sync_code_display.classes('font-mono text-3xl text-primary bg-gray-100 p-8 rounded-xl text-center')
                    ui.notify("Sync code generated! Use it on your other device.", type='positive')
                except Exception as e:
                    ui.notify(f"Error generating sync code: {e}", type='negative')

            ui.button("Generate Sync Code", 
                      on_click=generate_new_sync_code, 
                      icon='sync'
            ).props('size=lg color=accent').classes('w-full')

        # ==================== SECTION 2: Enter Sync Code ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">2. Enter Sync Code from Another Device</h2>')
            
            ui.label("Enter the Sync Code you received from another device:").classes('font-medium mb-4')

            sync_input = ui.input(
                label="Sync Code",
                placeholder="e.g. BLUE-APPLE-42"
            ).classes('w-full').props('uppercase')

            def claim_sync():
                if not sync_input.value.strip():
                    ui.notify("Please enter a sync code", type='warning')
                    return
                
                success = claim_sync_code(sync_input.value.strip())
                if success:
                    ui.notify("✅ Successfully linked to your account!", type='positive')
                    ui.navigate.to('/dashboard')
                else:
                    ui.notify("Invalid or expired sync code. Please check and try again.", type='negative')

            ui.button("Link This Device", 
                      on_click=claim_sync, 
                      icon='link'
            ).props('size=lg color=accent').classes('w-full mt-6')

        # ==================== SECTION 3: Real-time Editing ====================
        with ui.card().classes('w-full p-8 border border-warning'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Real-time Editing & Collaboration</h2>')
            
            ui.markdown("""
Real-time editing and collaboration works best in an environment that has this functionality mastered already. 

For this reason, **Niv Louie recommends**:

- **VS Code Live Share** for real-time Python code and script collaboration  
- **Microsoft 365** for real-time editing on Excel spreadsheets

Excel will allow saving as `.csv`, and **Niv Louie also supports Excel spreadsheets**.
            """).classes('text-base leading-relaxed')

        # ==================== SECTION 4: Your User ID ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Your User ID</h2>')
            ui.label("Use this User ID to sign in directly on any device:").classes('font-medium mb-3')
            
            ui.input(
                value=user_id,
                label="Your User ID"
            ).props('readonly').classes('w-full font-mono')

            ui.label("Tip: Save this User ID somewhere safe. You can also use a Sync Code instead.").classes('text-sm text-gray-600 mt-4')

        # Home button
        ui.button("Return to Home", 
                 on_click=lambda: ui.navigate.to("/")
        ).props('flat color=primary size=lg').classes('w-full mt-8')

        ui.label("More advanced collaboration features (fine-grained permissions, notifications) are planned for future updates.").classes('text-sm text-gray-500 mt-12 text-center')

    # Footer
    with ui.column().classes('w-full bg-gray-100 py-12 border-t mt-auto'):
        ui.label('© 2026 Niv Louie - Free and Open Source (GPL-3.0)').classes('text-xs text-gray-500 text-center mx-auto')