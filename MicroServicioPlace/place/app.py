from pyms.flask.app import Microservice

from place.models.init_db import db,ma

class MicroservicePlace(Microservice):
    def init_libs(self):
        db.init_app(self.application)
        ma.init_app(self.application)      
        with self.application.test_request_context():
            db.create_all()


def create_app():
    """Initialize the Flask app, register blueprints and intialize all libraries like Swagger, database, the trace system...
    return the app and the database objects.
    :return:
    """
    ms = MicroservicePlace(service="msplace", path=__file__)
    return ms.create_app()
