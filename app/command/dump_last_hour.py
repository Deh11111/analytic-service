import requests
from api.model.server import Server
from api.model.traffic import Traffic
from api.model.analytic import Analytic
import click
from flask.cli import with_appcontext
from app import db
from datetime import datetime, timedelta

# Creating a CLI command to dump data from the last hour     
@click.command('dump_last_hour')
@click.option('--time', default=1, help='Number of hours ago to dump data')
@with_appcontext
def dump_last_hour(time):
    # get all servers from the database
    servers = Server.query.all()
    # get all analytics from the database
    all_analytics = Analytic.query.all()
    
    # loop through each server and get its analytics
    for server in servers:
        # create a dictionary with key_id as the key and analytic as the value
        analytics_dict = {analytic.key_id: analytic for analytic in all_analytics if analytic.server_code == server.code}

        # build the Prometheus query
        url = f'http://{server.ip}/api/v1/query'
        query = f'sum by(access_key) (rate(shadowsocks_data_bytes[{time}h]))'

        # send the query to Prometheus
        response = requests.get(url, params={'query': query},auth=(server.login,server.password))
        data = response.json()['data']['result']
        
        # calculate the date range of the traffic data
        date_from = datetime.utcnow() - timedelta(hours=time)
        date_to = datetime.utcnow()

        # loop through each item in the response data
        for item in data:
             # if the item has an access_key metric, use it as the key_id
            if 'access_key' in item['metric']:
                key_id = item['metric']['access_key']
                analytic = analytics_dict.get(key_id)

                # skip key_id 0 (reserved for server statistics)
                if key_id == "0":
                    continue

                # if the analytic for the key_id doesn't exist, create it
                if analytic is None:
                    print(f"Analytic not found, creating new key:'{key_id}'Analytic")
                    analytic = Analytic(key_id=key_id, server_code=server.code)
                    db.session.add(analytic)
                    db.session.flush()
                    analytics_dict[key_id] = analytic

                # create a new traffic object and add it to the database session
                traffic = Traffic(analytic_id=analytic.id, bytes=int(float(item['value'][1])), date_from=date_from, date_to=date_to)
                db.session.add(traffic)

        # commit the changes to the database
        db.session.commit()
        print("Traffic was added")