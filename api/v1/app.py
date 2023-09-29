#!/usr/bin/python3
"""RESTful API implementantion"""
import os
from flask import Flask

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(exception):
    """method to handle app teardown"""
    storage.close()


if __name__ == '__main__':
    # Get host IP and port number
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')

    # Run the application
    app.run(host=host, port=port, threaded=True)
