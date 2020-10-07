from flask import Flask
app = Flask(__name__)

import Rest.models
import Rest.views
import Rest.Jwt