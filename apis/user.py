from typing import Any, Union

from email_validator import EmailNotValidError, validate_email
from flask import g, request
from flask_restx import Namespace, Resource, fields
from jsonschema import FormatChecker, ValidationError, validate

import model

api = Namespace("User", description="User tables", path="/")


study_model = api.model(
    "User",
    {
        "email_address": fields.String(required=True, default=""),
        "username": fields.String(required=True, default=""),
        "first_name": fields.String(required=True, default=""),
        "last_name": fields.String(required=True, default=""),
        "institution": fields.String(required=True, default=""),
        "orcid": fields.String(required=True, default=""),
        "location": fields.String(required=True, default=""),
        "timezone": fields.String(required=True, default=""),
        "profile_image": fields.String(required=False, default=""),
    },
)


@api.route("/user/profile")
class UserDetailsEndpoint(Resource):
    @api.doc(
        description="Returns user details gathered from the"
        " user and user_details tables"
    )
    @api.response(200, "Success", study_model)
    @api.response(400, "Validation Error")
    def get(self):
        """Returns user details"""
        user = model.User.query.get(g.user.id)
        user_details = user.user_details
        user_information = user.to_dict()
        # combine user and user_details to return a single object
        user_information.update(user_details.to_dict())
        return user_information, 200

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_model)
    def put(self):
        """Updates user details"""

        def validate_is_valid_email(instance):
            email_address = instance

            try:
                validate_email(email_address)
                return True
            except EmailNotValidError as e:
                raise ValidationError("Invalid email address format") from e

        # Schema validation
        # (profile_image is optional but additional properties are not allowed)
        schema = {
            "type": "object",
            "required": [
                "id",
                "email_address",
                "username",
                "first_name",
                "last_name",
                "institution",
                "orcid",
                "location",
                "timezone",
            ],
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string"},
                "email_address": {"type": "string", "format": "valid_email"},
                "username": {"type": "string", "minLength": 0},
                "first_name": {"type": "string", "minLength": 0},
                "last_name": {"type": "string", "minLength": 0},
                "institution": {"type": "string", "minLength": 0},
                "orcid": {"type": "string", "minLength": 0},
                "location": {"type": "string", "minLength": 0},
                "timezone": {"type": "string", "minLength": 0},
                "profile_image": {"type": "string", "minLength": 0},  # optional
            },
        }

        format_checker = FormatChecker()
        format_checker.checks("valid_email")(validate_is_valid_email)

        try:
            validate(
                instance=request.json, schema=schema, format_checker=format_checker
            )
        except ValidationError as e:
            # Verify if the user_information being sent
            # back is okay for this 400 error, e.message is
            # not being sent back
            return e.message, 400

        data: Union[Any, dict] = request.json
        user = model.User.query.get(g.user.id)
        # user.update(data) # don't update the username and email_address for now
        user_details = user.user_details
        user_details.update(data)
        model.db.session.commit()

        # combine user and user_details to return a single object
        user_information = user.to_dict()
        user_information.update(user_details.to_dict())
        return user_information
