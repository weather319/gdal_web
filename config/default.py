import os

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DATABASE_URI = os.path.join(basedir, 'app/app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')



if __name__ == "__main__":
    C = Config
    print (C.basedir)
    print (C.DATABASE_URI)