from flask import Flask
from mvc.controller.entry_controller import entry_bp
from mvc.model.database import init_db

app = Flask(__name__)
app.register_blueprint(entry_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)