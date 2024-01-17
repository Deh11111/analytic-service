from app import db
import datetime

# Model for recording analytic from prometheus servers
class Analytic(db.Model):
    # Name of model 
    __tablename__ = 'analytic'
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # ID of the user
    key_id = db.Column(db.String(100),nullable=False)
    # Server code. FK
    server_code = db.Column(db.String(255),db.ForeignKey('server.code'))
    # Date and time the record was created
    create_at = db.Column(db.DateTime,default=datetime.datetime.now())
    # Date and time the record was updated
    update_at = db.Column(db.DateTime,default=datetime.datetime.now())

    # Define a string representation of the model
    def __repr__(self):
        return 'Key:{}\nCode:{}\ndate_from:{}\n:date_to{}'.format(self.key_id,self.server_code,self.date_from,self.date_to)