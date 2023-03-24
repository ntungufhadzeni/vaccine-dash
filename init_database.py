from app import server, db
from models import Users
from werkzeug.security import generate_password_hash

with server.app_context():
    db.create_all()
    db.session.commit()
    user = Users('Ntungufhadzeni Mbudzeni', 'mbudzenin@yahoo.com', generate_password_hash('Nnrrr@123'), True)
    db.session.add(user)
    db.session.commit()

print('Done.')