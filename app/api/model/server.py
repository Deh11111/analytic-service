from app import db

# Model for recording prometheus servers
class Server(db.Model):
    # Name of model 
    __tablename__ = 'server'
    # Server code. PK
    code = db.Column(db.String(255), primary_key=True, unique=True)
    # IP address of the server
    ip = db.Column(db.String(64), index=True)
    # Login information of the server
    login = db.Column(db.String(120), index=True)
    # Password information of the server
    password = db.Column(db.String(120), index=True)

    # Define a string representation of the model
    def __repr__(self):
        return 'Code:{}\nIp:{}\nLoggin:{}\nPassword:{}'.format(self.code,self.ip,self.login,self.password)