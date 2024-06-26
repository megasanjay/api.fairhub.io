"""API routes for study status metadata"""

import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_status = api.model(
    "StudyStatus",
    {
        "id": fields.String(required=True),
        "overall_status": fields.String(required=True),
        "why_stopped": fields.String(required=True),
        "start_date": fields.String(required=True),
        "start_date_type": fields.String(required=True),
        "completion_date": fields.String(required=True),
        "completion_date_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/status")
class StudyStatusResource(Resource):
    """Study Status Metadata"""

    @api.doc("status")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_status)
    def get(self, study_id: int):
        """Get study status metadata"""
        study_ = model.Study.query.get(study_id)

        study_status_ = study_.study_status

        return study_status_.to_dict(), 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """Update study status metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "start_date",
                "start_date_type",
                "overall_status",
                "why_stopped",
                "completion_date",
                "completion_date_type",
            ],
            "properties": {
                "overall_status": {
                    "type": "string",
                    "minLength": 1,
                    "enum": [
                        "Withdrawn",
                        "Recruiting",
                        "Active, not recruiting",
                        "Not yet recruiting",
                        "Suspended",
                        "Enrolling by invitation",
                        "Terminated",
                        "Completed",
                    ],
                },
                "why_stopped": {"type": "string"},
                "start_date": {"type": "string", "minLength": 1},
                "start_date_type": {
                    "type": "string",
                    "enum": ["Actual", "Anticipated"],
                },
                "completion_date": {
                    "type": ["string", "null"],
                },
                "completion_date_type": {
                    "type": ["string", "null"],
                },
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[typing.Any, dict] = request.json
        if data["overall_status"] in ["Completed", "Terminated", "Suspended"]:
            if "why_stopped" not in data or not data["why_stopped"]:
                return (
                    f"why_stopped is required for overall_status: {data['overall_status']}",
                    400,
                )

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        study = model.Study.query.get(study_id)

        study.study_status.update(request.json)

        model.db.session.commit()

        return study.study_status.to_dict(), 200
