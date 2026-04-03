# pages/documentation.py - Academic Documentation / About Page

from nicegui import ui


@ui.page("/documentation")
def documentation():
    # Layout setup (consistent with other pages)
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label('Niv Louie').classes('text-3xl font-bold tracking-tight')
            ui.space()
            ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat color=accent')
            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).props('flat color=accent')
            ui.button('Collaborate', on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-12'):

        # Logo / Hero Image Area
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.card().classes('p-6 bg-transparent border-none shadow-none'):
                # Placeholder for logo/image - replace the src with your actual logo path later
                ui.image('https://via.placeholder.com/600x200/0B2A4D/FFFFFF?text=Niv+Louie+Logo').classes('max-w-md mx-auto rounded-xl')
                ui.label('Niv Louie').classes('text-5xl font-bold text-center text-primary mt-6 tracking-tight')

        # Academic Introduction
        ui.html('<h1 class="text-4xl font-bold text-center text-primary">Niv Louie: Advancing Braille Accessibility through Open Research and Technology</h1>')

        with ui.card().classes('p-10'):
            ui.markdown('''
Niv Louie is an open-source platform developed as part of a doctoral research initiative at Ariel University in collaboration with the Digital Pasts Lab. 

The project addresses a critical gap in assistive technology: the ability for educators, researchers, and blind users to rapidly create, test, and deploy high-quality Braille representations for any writing system or Unicode symbol set — including those without existing standardized Braille support.
            ''').classes('text-lg leading-relaxed')

        with ui.card().classes('p-10'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Research Context and Motivation</h2>')
            ui.markdown('''
Contemporary Braille translation tools are powerful but often rigid, requiring significant technical expertise and institutional resources to extend to new languages, specialized symbol sets (mathematics, chemistry, music, emojis), or emerging scripts. 

Niv Louie was conceived to democratize this process. By allowing users to upload simple CSV files containing Unicode characters, names, and desired Braille mappings, the system automatically generates Liblouis tables, test files, NVDA screen-reader extensions, and printable Braille documents.

This approach bridges traditional Braille scholarship with modern open-source software development, enabling rapid iteration and community-driven innovation while maintaining academic rigor and accessibility standards.
            ''')

        with ui.card().classes('p-10'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Core Objectives</h2>')
            ui.markdown('''
- **Empowerment**: Provide blind students, teachers, and researchers with tools to create custom Braille solutions without depending on proprietary software.
- **Interoperability**: Generate standards-compliant outputs for Liblouis and NVDA, ensuring seamless integration with existing assistive technology ecosystems.
- **Accessibility by Design**: Every feature is developed with direct input from blind users and follows universal design principles.
- **Open Scholarship**: Release all code, documentation, and generated resources under the GPL-3.0 license to foster global collaboration and reproducibility.
- **Educational Impact**: Serve as both a practical tool and a research instrument for studying Braille system development in digital contexts.
            ''')

        with ui.card().classes('p-10'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Open Source Philosophy</h2>')
            ui.markdown('''
Niv Louie is released as free and open-source software under the GNU General Public License (GPL-3.0). 

We believe that tools supporting disability access must themselves be accessible — both in usage and in their underlying code. By making the source fully transparent and modifiable, we invite contributions from linguists, computer scientists, Braille experts, and blind technologists worldwide.

The project is developed in Python using the NiceGUI framework, ensuring a clean, maintainable codebase that can evolve with community needs.
            ''')

        # Placeholder for future detailed instructions
        with ui.card().classes('p-10 bg-gray-50'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-primary">Detailed User Guide (Coming Soon)</h2>')
            ui.label('Comprehensive step-by-step instructions, tutorials, and technical documentation will be added in the next phase of development.').classes('text-gray-600')

    # Footer
    with ui.column().classes('w-full bg-gray-100 py-12 border-t mt-auto'):
        ui.label('© 2026 Niv Louie - Free and Open Source (GPL-3.0)').classes('text-xs text-gray-500 text-center mx-auto')
