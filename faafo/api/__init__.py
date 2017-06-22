from pkg_resources import resource_filename
import flask


def create_app(**kwargs):

    template_path = resource_filename(__name__, "templates")
    # Create the Flask app
    app = flask.Flask('faafo.api', template_folder=template_path)


    from .models import get_db, get_api
    db = get_db()
    db.init_app(app)


    # Configuration
    config_dict = kwargs.get('config_dict', None)

    if config_dict:
        app.config.update(config_dict)

    manager = get_api(db)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        manager.init_app(app)



    # Register blueprints
    from .service import mainPage
    app.register_blueprint(mainPage)
    # Restless api

    # Bootstrap(app)
    return app
