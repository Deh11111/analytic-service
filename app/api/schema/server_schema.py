from flask_marshmallow import Schema
from marshmallow.fields import String,Integer,DateTime,List

# Define the schema for the `Server` model
class ServerSchema(Schema):
    code = String()
    bytes = Integer()
    countries = List(String())
    create_at = DateTime(format='%Y-%m-%d %H:%M:%S')
    update_at = DateTime(format='%Y-%m-%d %H:%M:%S')