
# 🧠 Projet : Escape Game – Verrouillage de l’IA

Ce projet est un **mini escape game interactif** dans lequel les élèves doivent résoudre des énigmes mathématiques, dialoguer avec une IA, et corriger un programme Python pour stabiliser un système. Le tout se déroule dans une interface rétro stylisée à la manière d’un terminal.

---

## 🚀 Fonctionnalités

- Dialogue avec une IA personnalisée (OpenAI GPT-4o)
- Conservation d’un historique de conversation par **groupe**
- Énigme Python avec éditeur en ligne (CodeMirror)
- Résultats affichés en **console simulée**
- Message de fin dynamique si le verrouillage est réussi

---

## 📁 Structure des fichiers

```
.
├── app.py                      # Application principale Flask
├── .env                        # Contient la clé API OpenAI et la clé secrète Flask
├── requirements.txt            # Dépendances Python
├── static/
│   ├── style.css               # Styles rétro
├── scenario/
│   ├── scenario.txt            # Scénario initial de dialogue avec l’IA
│   ├── initial_prompt.txt      # Introduction du dialogue IA
│   └── message_fin.txt         # Message final affiché si succès
├── templates/
│   ├── login.html              # Page de connexion
│   ├── ia_interface.html       # Interface de dialogue IA
│   └── python_editor.html      # Éditeur Python avec mission
```

---

## ⚙️ Installation

1. **Cloner le dépôt**

```bash
git clone <url-du-depot>
cd escape_ia
```

2. **Créer un environnement virtuel (optionnel mais recommandé)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Créer un fichier `.env`**

```env
OPENAI_API_KEY=sk-...
FLASK_SECRET_KEY=une_clé_au_hasard
```

> ⚠️ Assure-toi d’avoir une clé OpenAI valide (GPT-4o activé).

---

## ▶️ Lancer l’application

```bash
python app.py
```

Ensuite, ouvre [http://localhost:5000](http://localhost:5000) dans ton navigateur.

---

## 🧪 Identifiants de connexion

- **Code d’accès** : `1234`  
  _(modifiable dans `app.py` si besoin)_

---

## 🎯 Objectifs pédagogiques

- Stimuler la logique via une énigme mathématique (intégrale)
- Travailler la compréhension de code Python
- Favoriser la collaboration autour d’un scénario immersif
- Découvrir l’interface GPT en contexte guidé

---

## 🛠️ Personnalisation

- Pour modifier l’énigme Python, va dans `python_editor.html`
- Pour adapter le scénario IA, modifie `static/scenario.txt` et `static/initial_prompt.txt`
- Le message final de réussite est dans `static/message_fin.txt`

---

## 📍 Auteur

Projet conçu avec ❤️ par [TonNom] pour une utilisation pédagogique en lycée.
