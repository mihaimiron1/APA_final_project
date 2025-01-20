from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = '564521751a02c0e0e5f324d5a850a38e6ba1873a7a1e3027'  # Pentru sesiuni și mesaje flash

# Citirea fișierului JSON cu utilizatori    

def load_users():
    try:
        with open('login_users.json', 'r') as file:
            return json.load(file)['users']
    except FileNotFoundError:
        flash("Fișierul cu utilizatori nu a fost găsit.", 'error')
        return []
    except json.JSONDecodeError:
        flash("Fișierul JSON nu este valid.", 'error')
        return []





# Ruta pentru pagina de conectare
@app.route('/conectare', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()
        user_found = None

        # Căutăm utilizatorul în fișierul JSON
        for user in users:
            if user['Email'] == email and user['Parola'] == password:
                user_found = user
                break

        if user_found:
            user_id = user_found['ID']
            return redirect(url_for('home', user_id=user_id))  # Redirecționează la pagina următoare cu ID-ul utilizatorului
        else:
            flash("Persoana nu a fost înregistrată. Verificați email-ul și parola!", 'error')

    return render_template('conect.html')

# Ruta pentru pagina principală după logare
@app.route('/home/<int:user_id>')
def home(user_id):
    return f"Bine ai venit! ID-ul tău este {user_id}."

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/')
def index():
    return render_template('index.html')  # Asigură-te că ai un fișier 'index.html' în directorul 'templates'
