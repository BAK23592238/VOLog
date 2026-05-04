from flask import Flask
from flask_cors import CORS
from mvc.model.database import init_db
from mvc.controller.entry_controller import entry_bp

app = Flask(__name__)

# allow requests from other origins
CORS(app)

# register routes from entry crontroller
app.register_blueprint(entry_bp)

if __name__ == '__main__':

    # initialise database before starting the app
    init_db()

    # run in debug mode for development
    app.run(debug=True)