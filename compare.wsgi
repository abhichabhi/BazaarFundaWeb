import os, sys, logging
logging.basicConfig(stream=sys.stderr)

PROJECT_DIR = '/var/www/html/bazaarfunda/phone-compare'
VIRTUAL_EV = '/home/ubuntu/compare/env'
activate_this = os.path.join(VIRTUAL_EV, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from app import app as application