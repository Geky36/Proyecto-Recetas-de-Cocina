from flask import Flask
from routes.route import router  # Importamos el Blueprint

app = Flask(__name__)

# Registramos el Blueprint
app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug=True)
