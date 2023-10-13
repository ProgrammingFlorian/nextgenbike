from flask import Flask

application = Flask(__name__)

from backend.server.app import routes