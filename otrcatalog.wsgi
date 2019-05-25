# otrcatalog.wsgi in /var/www/flaskapp/udacity_deploy_linux

import sys

# Add app code directory to path.
sys.path.insert(0, '/var/www/flaskapp/udacity_deploy_linux')

from application import app as application
application.config['SECRET_KEY'] = "secret key here"
