import os


def create_local_db(app,db):
    if not os.path.exists('instance/data.db'):
        with app.app_context():
            db.create_all()


