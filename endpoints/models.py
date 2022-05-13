from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class User(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(265), nullable = False)
    password = database.Column(database.String(265), nullable = False)


    def __repr__ ( self ):
        return "{} {}".format(self.forename, self.surname)

