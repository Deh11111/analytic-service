from http import HTTPStatus
from flask import request
from api.schema.response_schema import SuccessSchema,ErrorSchema
from api.schema.server_schema import ServerSchema
from api.model.traffic import Traffic
from api.model.analytic import Analytic
from api.model.server import Server
from flasgger import swag_from
from datetime import date, time, datetime
from flask import Blueprint

# Create a Blueprint object to define the traffic API endpoints
api = Blueprint('api_analytic', __name__)
# Define the GET method for retrieving traffic data
@api.route('/<string:server_code>', methods=['GET'])
# Use Swagger to document the endpoint with parameters and responses
@swag_from({
    'parameters': [
        {
            'in': 'path',
            'name': 'server_code',
            'description': 'The server code to get analytics for',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'in': 'query',
            'name': 'date_from',
            'description': 'The start date to filter analytics by',
            'required': False,
            'schema': {
                'type': 'string',
                'format': 'date-time'
            }
        },
        {
            'in': 'query',
            'name': 'date_to',
            'description': 'The end date to filter analytics by',
            'required': False,
            'schema': {
                'type': 'string',
                'format': 'date-time'
            }
        }
    ],
    'responses': {
        # Indicates that the operation was successful, and data is being returned.
        HTTPStatus.OK.value: {
            'description': 'Success'
        },
        # Indicates that the request contained invalid data, and the operation could not be completed
        HTTPStatus.BAD_REQUEST.value: {
            'description': 'Error'
        },
        # Indicates that the requested resource (server or traffic key) could not be found
        HTTPStatus.NOT_FOUND.value: {
            'description': 'Not found'
        }
    }
})

# Get traffic data from the server
def get_server(server_code):
    try:
        # set default date range to today's date
        date_from = datetime.combine(date.today(), time.min)
        date_to = datetime.combine(date.today(), time.max)
        
        # check if date range is specified in the query parameters      
        if request.args:
            data = request.args.to_dict()
            if 'date_from' in data:
                date_from = datetime.strptime(data['date_from'], '%Y-%m-%d %H:%M:%S')
            if 'date_to' in data:
                date_to = datetime.strptime(data['date_to'], '%Y-%m-%d %H:%M:%S')
        
        # retrieve traffic data for the specified server within the date range  
        traffic = Traffic.query.join(Analytic)\
            .filter(Analytic.server_code == server_code,\
                    Traffic.date_from >= date_from,\
                    Traffic.date_to <= date_to)\
            .all()
        # return 404 error if no traffic data is found
        if len(traffic) == 0 :
            error_schema = ErrorSchema() 
            error_schema.code = 404
            error_schema.message = f"This server: '{server_code}' not finded"
            result = error_schema.dump(error_schema)
            return result,HTTPStatus.NOT_FOUND
        
        # calculate total bytes and countries from the retrieved traffic data
        total_bytes = sum(t.bytes for t in traffic)
        total_countries = list(set([t.country_code for t in traffic]))

        # create schemas to serialize the response data
        schema = ServerSchema()
        schema.code = server_code
        schema.bytes = total_bytes
        schema.countries = total_countries
        schema.create_at = date_from
        schema.update_at = date_to
        
        result_schema = SuccessSchema()
        result_schema.result = schema.dump(schema)
        result = result_schema.dump(result_schema)

        return result,HTTPStatus.OK

    except Exception as ex:
        # catch any exceptions and return 500 Bad request and message of exception
        error_schema = ErrorSchema()
        error_schema.code = 500
        error_schema.message = str(ex)
        result = error_schema.dump(error_schema)
        return result,HTTPStatus.BAD_REQUEST