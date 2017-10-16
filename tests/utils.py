

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object('config.Config')
    import os
    app.secret_key = os.urandom(24)


    return app