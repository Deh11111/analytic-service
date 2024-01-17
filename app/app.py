import time 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config
from flasgger import Swagger
import pymysql

# Initializing database object
db = SQLAlchemy()

# Creating the Flask application object and setting the configuration
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # setting up Swagger API documentation and registering the blueprints
    app.config['SWAGGER'] = {
        'title': 'Analytic service',
    }
    swagger = Swagger(app)

    #initilization database and migration 
    db.init_app(app)
    migration = Migrate(app,db)
    
    # declaring API Routes
    from api.routes import key_analytic_api,traffic_analytic_api
    
    app.register_blueprint(key_analytic_api, url_prefix='/api/v1')
    app.register_blueprint(traffic_analytic_api, url_prefix='/api/v1')
    # checks the connection to a database and tries to reconnect if the connection fails
    check_db_connection(app,db)

    from command.dump_last_hour import dump_last_hour

    app.cli.add_command(dump_last_hour)
    
    return app

def check_db_connection(app,db):
    while True:
        with app.app_context():
            try:
                pymysql.connect(
                    host = Config.MYSQL_HOST,
                    user = Config.MYSQL_USER,
                    password = Config.MYSQL_PASSWORD,
                    database = Config.MYSQL_DATABASE,
                    port = int(Config.MYSQL_PORT),
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("Connection to database is successful")
                return True
            except Exception as e:
                print("Wait connect to database 10 seconds")
                print(e)
                time.sleep(10)


# Running the Flask application
if __name__ == '__main__':
    app = create_app()
    
    host = Config.HOST
    port = Config.PORT
    debug = Config.DEBUG

    app.run(host=host, port=port, debug=debug)