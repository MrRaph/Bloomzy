from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    @app.route('/auth/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        recaptcha = data.get('recaptcha_token')

        # Vérification des champs obligatoires
        if not email or not password:
            return jsonify({'error': 'Champs obligatoires manquants'}), 400

        # Vérification du format email
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Email invalide'}), 400

        # Vérification de la force du mot de passe
        if len(password) < 8 or password.isdigit() or password.isalpha():
            return jsonify({'error': 'Mot de passe trop faible'}), 400

        # Protection contre les bots (reCAPTCHA simulé)
        if recaptcha is None:
            return jsonify({'error': 'Captcha requis'}), 400

        # Simuler la gestion d'un email déjà utilisé (en mémoire)
        if not hasattr(app, 'users'):
            app.users = set()
        if email in app.users:
            return jsonify({'error': 'Email existe déjà'}), 409
        app.users.add(email)

        # Réponse succès
        return jsonify({
            'id': len(app.users),
            'email': email
        }), 201

    return app
