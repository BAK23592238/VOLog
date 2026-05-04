# 
from flask import Flask
from flask_cors import CORS
from mvc.model.database import init_db
from mvc.controller.entry_controller import entry_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(entry_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)