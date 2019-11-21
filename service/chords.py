import datetime
import enum
from flask import g, Flask

from common.config import conf
app = Flask(__name__)

def fetch_sites():
    #GET get a site from chords service
    return "sites fetched"

def fetch_site(site_id):
    #GET get a site from chords service
    return "site fetched" + site_id

def create_site():
    #POST to chords service to creat a new sites
    return "site created" + site_id

def update_site(site_id):
    #PUT to chords service to update the site informationa
    return "site updated" + site_id

def delete_site(site_id):
    #DELETE to chords servive to remove site
    return "site deleted" + site_id
