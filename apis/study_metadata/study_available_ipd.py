"""API routes for study available ipd metadata"""
import typing

from flask import request
from flask_restx import Resource, fields

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_available = api.model(
    "StudyAvailable",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "type": fields.String(required=True),
        "comment": fields.String(required=True),
        "url": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/available-ipd")
class StudyAvailableResource(Resource):
    """Study Available Metadata"""

    @api.doc("available")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_available)
    def get(self, study_id: int):
        """Get study available metadata"""
        study_ = model.Study.query.get(study_id)

        study_available_ipd_ = study_.study_available_ipd

        sorted_study_available_ipd = sorted(
            study_available_ipd_, key=lambda x: x.created_at
        )

        return [s.to_dict() for s in sorted_study_available_ipd]

    @api.doc("update available")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_available)
    def post(self, study_id: int):
        """Create study available metadata"""
        study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403
        data: typing.Union[dict, typing.Any] = request.json
        study_obj = model.Study.query.get(study_id)

        list_of_elements = []

        for i in data:
            if "id" in i and i["id"]:
                study_available_ipd_ = model.StudyAvailableIpd.query.get(i["id"])
                study_available_ipd_.update(i)
                list_of_elements.append(study_available_ipd_.to_dict())
            elif "id" not in i or not i["id"]:
                study_available_ipd_ = model.StudyAvailableIpd.from_data(study_obj, i)
                model.db.session.add(study_available_ipd_)
                list_of_elements.append(study_available_ipd_.to_dict())

        model.db.session.commit()

        return list_of_elements


@api.route("/study/<study_id>/metadata/available-ipd/<available_ipd_id>")
class StudyLocationUpdate(Resource):
    """Study Available Metadata"""

    def delete(self, study_id: int, available_ipd_id: int):
        """Delete study available metadata"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_available_ = model.StudyAvailableIpd.query.get(available_ipd_id)

        model.db.session.delete(study_available_)
        model.db.session.commit()

        return 204
