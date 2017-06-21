from pkg_resources import resource_filename
import flask


def create_app(**kwargs):

    template_path = resource_filename(__name__, "templates")
    # Create the Flask app
    app = flask.Flask('faafo.api', template_folder=template_path)
    from .models import db
    db.init_app(app)

    # Configuration
    config_dict = kwargs.get('config_dict', None)

    if config_dict:
        app.config.update(config_dict)

    # Register blueprints
    from .service import mainPage

    app.register_blueprint(mainPage)

    # Bootstrap(app)
    return app
