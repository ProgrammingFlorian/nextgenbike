from flask import Flask

app = Flask(__name__)

from backend.server.app import routes