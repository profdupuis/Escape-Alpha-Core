from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from markupsafe import Markup
import openai
import os
import uuid
from dotenv import load_dotenv
from flask_session import Session
import random
from io import StringIO
import sys

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)
# Clé secrète pour gérer les sessions Flask
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")

# Configuration de Flask-Session pour stocker les sessions côté serveur (fichier)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Clé API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Liste des noms de groupes possibles
groupes_possibles = [f"Groupe {i}" for i in range(1, 100)]

# Écritures valides du code d'accès initial
codes_valides = ['ln(5)+3', '3+ln(5)']

# Avant chaque requête, vérifie et initialise la session si nécessaire
@app.before_request
def setup_session():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]
        session['groupe'] = random.choice(groupes_possibles)
        print(f"🆕 Nouvelle session : {session['user_id']} → {session['groupe']}")

# Page d'accueil avec formulaire de code d'accès
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['code'] in codes_valides:
            return redirect(url_for('interface_ia'))
        else:
            error = 'Accès refusé'
    return render_template('login.html', error=error)

# Interface principale de l'IA
@app.route('/ia')
def interface_ia():
    with open("scenario/initial_prompt.txt", "r", encoding="utf-8") as f:
        initial_message = Markup("<br>".join(f.read().strip().splitlines()))
    return render_template('ia_interface.html', initial_message=initial_message)

# Éditeur Python avec la mission finale
@app.route('/python')
def python_editor():
    return render_template('python_editor.html')

# API de dialogue avec l'IA (appelée en POST depuis l'interface)
@app.route('/api/message', methods=['POST'])
def api_message():
    user_message = request.json.get('message')

    # Si groupe non encore défini
    if 'groupe' not in session:
        session['groupe'] = f"Groupe {uuid.uuid4().int % 100}"

    # Initialiser l'historique de conversation si première requête
    if 'history' not in session:
        with open('scenario/scenario.txt', 'r', encoding='utf-8') as f:
            scenario = f.read().replace("{groupe}", session['groupe'])
        session['history'] = [{"role": "system", "content": scenario}]

    # Ajouter le message utilisateur à l'historique
    session['history'].append({"role": "user", "content": user_message})

    # Envoi de la requête à OpenAI avec tout l'historique
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=session['history']
    )

    # Réponse de l'IA
    reply = response.choices[0].message.content
    session['history'].append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

# Vérification du code Python exécuté dans la page /python
@app.route('/verifier_code', methods=['POST'])
def verifier_code():
    data = request.json
    code = data.get('code', '')
    local_vars = {}
    
    # Capture la sortie standard de l'exécution
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        # Exécution du code fourni
        exec(code, {}, local_vars)
        output = redirected_output.getvalue().strip() or "(aucune sortie)"
        
        # Vérifie si le tableau 'bloques' contient la bonne réponse
        if 'bloques' in local_vars and local_vars['bloques'] == [84, 51]:
            with open("scenario/message_fin.txt", "r", encoding="utf-8") as f:
                message_fin = f.read()
            return jsonify(success=True, message="🎉 Verrouillage confirmé ! Mission accomplie.", output=output, fin=message_fin)
        else:
            return jsonify(success=False, message="🔁 Les processus bloqués ne sont pas corrects.", output=output)
    except Exception as e:
        # Gestion des erreurs d'exécution
        return jsonify(success=False, message=f"Erreur d'exécution côté serveur : {e}", output=redirected_output.getvalue().strip() or "(aucune sortie)")
    finally:
        # Restaure la sortie standard
        sys.stdout = old_stdout

# Permet de réinitialiser la session en redémarrant depuis la page IA
@app.route('/reset')
def reset_session():
    session.clear()
    return redirect(url_for('interface_ia'))

# Lancement de l'application Flask en mode debug
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
