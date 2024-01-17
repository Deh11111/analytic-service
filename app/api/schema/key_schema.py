from flask_marshmallow import Schema
from marshmallow.fields import String,Integer,DateTime,Nested,List

# Define the schema for the data of prometheus
class KeySchema(Schema):
    id = Integer()
    bytes = Integer()
    countries = List(String())
    # Date and time when the key was first used
    date_from = DateTime(format='%Y-%m-%d %H:%M:%S')
    # Date and time when the key was last used
    date_to = DateTime(format='%Y-%m-%d %H:%M:%S')

# Define the schema for the `Analytic` model
class AnalyticSchema(Schema):
    server = String()
    key = Nested(KeySchema)