from app import db
import datetime

# Model for recording user traffic for a certain time
class Traffic(db.Model):
    # Name of model 
    __tablename__ = 'traffic'
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to Analytic
    analytic_id = db.Column(db.Integer,db.ForeignKey('analytic.id'))
    # Amount of traffic in bytes
    bytes = db.Column(db.Float)
    # Start time of traffic data measurement
    date_from = db.Column(db.DateTime,default=datetime.datetime.now())
    # End time of traffic data measurement
    date_to = db.Column(db.DateTime,default=datetime.datetime.now())
    # Country code. Optional
    country_code = db.Column(db.String(100),nullable=True) 
    
    # Define a string representation of the model
    def __repr__(self):
        return 'analytic_key:{}'.format(self.analytic_id)