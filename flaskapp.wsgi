import sys,os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/goslow/app/")
sys.path.insert(0,"/var/www/goslow/app/models/")
os.chdir("/var/www/goslow")
from app import app as application
application.secret_key = 'Add your secret key'
