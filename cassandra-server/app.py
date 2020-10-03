# Import Statements
from flask import Flask
from users import user_api
from polls import poll_api

# Flask application
app = Flask(__name__)

# Resgistration of users and polls blueprints
app.register_blueprint(user_api, url_prefix = '/users')
app.register_blueprint(poll_api, url_prefix = '/polls')


if __name__ == "__main__":
    app.run(debug = True)