# pages/13_collaborate.py

from nicegui import ui, app
from utils.storage import ensure_user_directories
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        print("LOG: User storage initialized from collaborate page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/collaborate")
def collaborate():
    init_user_storage()

    with ui.column().classes('w-full max-w-4xl mx-auto p-8 gap-10'):
        
        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back", 
                     on_click=ui.navigate.back).props('flat color=primary size=lg')
            
            ui.html('<h1 class="text-3xl font-bold text-primary">Collaborate with Others</h1>')

        ui.markdown("""
This page allows you to share your Niv Louie projects with others and access projects shared with you.
        """).classes('text-base leading-relaxed')

        # ==================== SECTION 1: Share Project ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">1. Share One of Your Projects</h2>')

            project_select = ui.select(
                options=sorted(project.languages_list),
                label="Select Project to Share",
                with_input=True
            ).classes('w-full mb-6')

            ui.label("Permission Level").classes('font-medium mb-3 text-primary')
            share_type = ui.radio(['Read Only', 'Read + Write'], value='Read Only').props('inline').classes('mb-6')

            def generate_share_link():
                if not project_select.value:
                    ui.notify("Please select a project first", type='warning')
                    return
                
                user_id = app.storage.user.get("user_id", "unknown")
                share_url = f"http://localhost:8080/view_shared?user={user_id}&project={project_select.value}&perm={share_type.value.lower().replace(' ', '_')}"

                ui.notify("Share link generated successfully!", type='positive')
                
                with ui.dialog() as dlg, ui.card().classes('w-full max-w-lg'):
                    ui.html('<h3 class="font-bold mb-3 text-primary">Your Share Link</h3>')
                    ui.input(value=share_url).props('readonly').classes('w-full')
                    ui.button("Copy Link", on_click=lambda: ui.notify("Link copied to clipboard")).props('color=accent')
                    ui.button("Close", on_click=dlg.close).props('flat color=primary')
                dlg.open()

            ui.button("Generate Share Link", 
                      on_click=generate_share_link, 
                      icon='share'
            ).props('size=lg color=accent').classes('w-full')

        # ==================== SECTION 2: Access Shared Projects ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">2. How to Access Shared Projects</h2>')

            with ui.row().classes('gap-8'):
                with ui.column().classes('flex-1'):
                    ui.html('<h3 class="font-semibold mb-3 text-primary">Sign in on Another Device</h3>')
                    ui.markdown("""
1. Open Niv Louie on the new device  
2. Go to **Collaborate** page  
3. Enter your **User ID** below  
4. Your projects will appear automatically
                    """)

                with ui.column().classes('flex-1'):
                    ui.html('<h3 class="font-semibold mb-3 text-primary">Using a Shared Link</h3>')
                    ui.markdown("""
1. Click the shared link you received  
2. The project will open directly (if you have permission)  
3. You may be asked to sign in with your own User ID
                    """)

            ui.separator().classes('my-8')

            ui.label("Your User ID (use this to sign in on other devices)").classes('font-medium mb-2')
            ui.input(
                value=app.storage.user.get("user_id", "Not available yet")
            ).props('readonly').classes('w-full mb-6')

            ui.label("Enter Sharer’s User ID to access their shared projects").classes('font-medium mb-2')
            shared_user_id = ui.input(
                label="Sharer’s User ID",
                placeholder="Paste the User ID here..."
            ).classes('w-full mb-4')

            shared_project = ui.input(
                label="Specific Project Name (optional)",
                placeholder="Leave blank to see all shared projects"
            ).classes('w-full mb-6')

            def load_shared_projects():
                if not shared_user_id.value.strip():
                    ui.notify("Please enter the sharer’s User ID", type='warning')
                    return
                ui.notify(f"Searching for projects from User ID: {shared_user_id.value}", type='info')
                ui.notify("Shared project loading will be implemented soon", type='positive')

            ui.button("Load Shared Projects", 
                      on_click=load_shared_projects, 
                      icon='cloud_download'
            ).props('size=lg color=accent').classes('w-full')

        # ==================== SECTION 3: Your Shared Projects ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">3. Your Shared Projects</h2>')
            
            shared_list = ui.column().classes('w-full gap-3')

            with shared_list:
                if not project.languages_list:
                    ui.label("You haven't shared any projects yet.").classes('italic text-gray-500')
                else:
                    for proj in sorted(project.languages_list)[:8]:
                        with ui.row().classes('items-center justify-between w-full p-4 border rounded-lg'):
                            ui.label(proj).classes('flex-grow font-medium')
                            ui.button('Generate New Link', 
                                      on_click=lambda p=proj: generate_share_link_for_project(p)
                            ).props('flat color=accent')

        # Home button
        ui.button("Return to Home", 
                 on_click=lambda: ui.navigate.to("/")
        ).props('flat color=primary size=lg').classes('w-full mt-8')

        ui.label("More advanced collaboration features (real-time editing, permission management, notifications) are planned.").classes('text-sm text-gray-500 mt-12 text-center')


# Helper function
def generate_share_link_for_project(project_name):
    user_id = app.storage.user.get("user_id", "unknown")
    share_url = f"http://localhost:8080/view_shared?user={user_id}&project={project_name}&perm=read_only"
    
    with ui.dialog() as dlg, ui.card().classes('w-full max-w-lg'):
        ui.html(f'<h3 class="font-bold mb-3 text-primary">Share Link for {project_name}</h3>')
        ui.input(value=share_url).props('readonly').classes('w-full')
        ui.button("Copy Link", on_click=lambda: ui.notify("Link copied to clipboard")).props('color=accent')
        ui.button("Close", on_click=dlg.close).props('flat color=primary')
    dlg.open()