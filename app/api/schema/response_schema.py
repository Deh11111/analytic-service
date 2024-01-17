from flask_marshmallow import Schema
from marshmallow.fields import String,Integer,Dict


# Define success response schema
class SuccessSchema(Schema):
    status = String(default='success')
    result = Dict() 
    message = String(default='')

# Define error response schema
class ErrorSchema(SuccessSchema):    
    status = String(default="error")
    code = Integer()