from flask import Flask

# Create Flask application
app = Flask(__name__)

from backend import routes  # This import must stay after app is created
