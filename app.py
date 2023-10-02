"""Entry point for the application."""
from flask import Flask, request, make_response, g
import jwt
import config
from flask_cors import CORS
from sqlalchemy import MetaData
from datetime import timezone
import datetime

import model
from apis import api
from flask_bcrypt import Bcrypt
from apis.authentication import authentication, authorization, UnauthenticatedException, AccessDenied

# from pyfairdatatools import __version__

bcrypt = Bcrypt()


def create_app():
    """Initialize the core application."""
    # create and configure the app
    app = Flask(__name__)
    # `full` if you want to see all the details
    app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"
    app.config["RESTX_MASK_SWAGGER"] = False
    # Initialize config
    app.config.from_pyfile("config.py")
    # app.register_blueprint(api)

    # TODO - fix this
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    app.config.from_prefixed_env("FAIRHUB")

    # print(app.config)

    # TODO: add a check for secret key

    if "DATABASE_URL" in app.config:
        # if "TESTING" in app_config and app_config["TESTING"]:
        #     pass
        # else:
        #   print("DATABASE_URL: ", app.config["DATABASE_URL"])
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    else:
        # throw error
        raise RuntimeError("FAIRHUB_DATABASE_URL not set")

    model.db.init_app(app)
    api.init_app(app)
    bcrypt.init_app(app)

    # Only allow CORS origin for localhost:3000
    CORS(
        app,
        resources={
            "/*": {
                "origins": [
                    "http://localhost:3000",
                ],
            }
        },
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Credentials",
        ],
        supports_credentials=True,
    )

    # CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})

    #
    # @app.cli.command("create-schema")
    # def create_schema():
    #     engine = model.db.session.get_bind()
    #     metadata = MetaData()
    #     metadata.reflect(bind=engine)
    #     table_names = [table.name for table in metadata.tables.values()]
    #     print(table_names)
    #     if len(table_names) == 0:
    #         with engine.begin() as conn:
    #             """Create the database schema."""
    #             model.db.create_all()

    @app.before_request
    def on_before_request():
        try:
            authentication()
            authorization()
        except AccessDenied:
            return "Authentication is required", 401

    @app.after_request
    def on_after_request(resp):
        if "token" not in request.cookies:
            return resp
        token = request.cookies.get("token")
        try:
            decoded = jwt.decode(token, config.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            resp.delete_cookie("token")
            return resp
        token_blacklist = model.TokenBlacklist.query.get(decoded["jti"])
        if token_blacklist:
            resp.delete_cookie("token")
            return resp
        expired_in = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
        new_token = jwt.encode({"user": decoded["user"], "exp": expired_in, "jti": decoded["jti"]}, config.secret, algorithm="HS256")
        resp.set_cookie("token", new_token, secure=True, httponly=True, samesite="lax")
        return resp

    @app.cli.command("destroy-schema")
    def destroy_schema():
        engine = model.db.session.get_bind()
        with engine.begin() as conn:
            """Create the database schema."""
            model.db.drop_all()

    with app.app_context():
        engine = model.db.session.get_bind()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        table_names = [table.name for table in metadata.tables.values()]
        # print(table_names)
        if len(table_names) == 0:
            with engine.begin() as conn:
                """Create the database schema."""
                model.db.create_all()
    return app


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host="0.0.0.0", port=port)
