from flask import Flask, render_template

import logging


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_url_path="",
        static_folder="static",
    )

    app.config.from_pyfile("default_settings.py")
    app.config.from_pyfile("config.py", silent=True)

    if app.config["DEBUG"] or app.config["ENV"] == "development":
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warn(f"Page not found: {e}")
        return render_template("error.html"), 404

    from pangea_demo.blueprints.index import main as main_blueprint
    from pangea_demo.blueprints.api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
