from flask import Flask
from sqlalchemy_utils import database_exists, create_database, drop_database
import shutil
from flask_migrate import Migrate, init, migrate, upgrade

from configuration import Configuration
from models import database

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

# if ( not database_exists ( application.config["SQLALCHEMY_DATABASE_URI"] ) ):
#    create_database ( application.config["SQLALCHEMY_DATABASE_URI"] );


print("------------------------------------------------------------------------------------")
if (not database_exists(Configuration.SQLALCHEMY_DATABASE_URI)):
    create_database(Configuration.SQLALCHEMY_DATABASE_URI)
    print("Kreirana baza podataka!")
else:
    drop_database(Configuration.SQLALCHEMY_DATABASE_URI)
    create_database(Configuration.SQLALCHEMY_DATABASE_URI)
    print("Baza podataka izbrisana i ponovo kreirana!!")
print("------------------------------------------------------------------------------------")

database.init_app(application)

with application.app_context() as context:
    mydir = "migrations"

    try:
        shutil.rmtree(mydir)
    except OSError as e:
        print("Ne postoji folder /migrations")

    init()
    migrate(message="Initial migration")
    upgrade()

    print("Baza podataka inicijalizovana!")
