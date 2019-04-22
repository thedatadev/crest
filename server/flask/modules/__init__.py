from flask import Flask

from modules.test_module.routes import mod as test_mod

app = Flask(__name__)

app.register_blueprint(test_mod)