from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from datetime import datetime

# Translation Dictionary
RESPONSES = {
    'english': {
        'help': """Available commands:
  about     - Who am I?
  projects  - View my work
  skills    - What I can do
  contact   - Get in touch
  language  - Change language (deutsch/english)
  clear     - Clear the terminal
  date      - Current date and time
  help      - Show this help message""",
        'about': """Hello! I'm a Django Terminal Homepage.
I was created to demonstrate a simple, text-based interface on the web.
I enjoy minimalistic design and efficient code.""",
        'projects': """1. Django Terminal: This website!
2. AI Chatbot: A Python-based CLI assistant.
3. E-commerce Platform: Built with React and Node.js.""",
        'skills': """Languages: Python, JavaScript, HTML, CSS, SQL
Frameworks: Django, React, Flask
Tools: Git, Docker, Linux""",
        'contact': """Email: user@example.com
GitHub: github.com/user
Twitter: @user""",
        'not_found': "Command not found: {}. Type 'help' for available commands.",
        'lang_switched': "Language switched to English."
    },
    'german': {
        'help': """Verfügbare Befehle:
  about     - Wer bin ich?
  projects  - Meine Projekte
  skills    - Meine Fähigkeiten
  contact   - Kontakt
  language  - Sprache ändern (deutsch/english)
  clear     - Terminal leeren
  date      - Datum und Uhrzeit
  help      - Hilfe anzeigen""",
        'about': """Hallo! Ich bin eine Django Terminal Homepage.
Ich wurde erstellt, um eine einfache Text-Schnittstelle im Web zu demonstrieren.
Ich mag minimalistisches Design und effizienten Code.""",
        'projects': """1. Django Terminal: Diese Webseite!
2. KI Chatbot: Ein Python-basierter CLI Assistent.
3. E-Commerce Plattform: Gebaut mit React und Node.js.""",
        'skills': """Sprachen: Python, JavaScript, HTML, CSS, SQL
Frameworks: Django, React, Flask
Tools: Git, Docker, Linux""",
        'contact': """E-Mail: user@example.com
GitHub: github.com/user
Twitter: @user""",
        'not_found': "Befehl nicht gefunden: {}. Geben Sie 'help' ein für verfügbare Befehle.",
        'lang_switched': "Sprache zu Deutsch geändert."
    }
}

@ensure_csrf_cookie
def index(request):
    return render(request, 'terminal/index.html')

def handle_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command', '').strip().lower()
            
            # Get current language from session, default to english
            current_lang = request.session.get('language', 'english')
            
            response_text = ""

            # Language switching logic
            if command == 'deutsch':
                request.session['language'] = 'german'
                current_lang = 'german' # Update local var for immediate use if needed, or just return switch msg
                response_text = RESPONSES['german']['lang_switched']
            
            elif command == 'english':
                request.session['language'] = 'english'
                current_lang = 'english'
                response_text = RESPONSES['english']['lang_switched']

            elif command == 'language':
                 if current_lang == 'english':
                     response_text = "Current language: English. Type 'deutsch' to switch."
                 else:
                     response_text = "Aktuelle Sprache: Deutsch. Geben Sie 'english' ein um zu wechseln."

            # Dynamic commands based on language
            elif command in ['about', 'projects', 'skills', 'contact', 'help']:
                response_text = RESPONSES[current_lang][command]
            
            elif command == 'date':
                response_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            elif command == '':
                response_text = ""

            else:
                response_text = RESPONSES[current_lang]['not_found'].format(command)

            return JsonResponse({'output': response_text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
