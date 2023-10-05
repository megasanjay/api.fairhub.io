"""API routes for study ipdsharing metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db
from ..authentication import is_granted


from apis.study_metadata_namespace import api


study_ipdsharing = api.model(
    "StudyIpdsharing",
    {
        "id": fields.String(required=True),
        "ipd_sharing": fields.String(required=True),
        "ipd_sharing_description": fields.String(required=True),
        "ipd_sharing_info_type_list": fields.List(fields.String, required=True),
        "ipd_sharing_time_frame": fields.String(required=True),
        "ipd_sharing_access_criteria": fields.String(required=True),
        "ipd_sharing_url": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/ipdsharing")
class StudyIpdsharingResource(Resource):
    """Study Ipd sharing Metadata"""

    @api.doc("ipdsharing")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_ipdsharing)
    def get(self, study_id: int):
        """Get study ipdsharing metadata"""
        study_ = Study.query.get(study_id)

        return study_.study_ipdsharing.to_dict()

    def put(self, study_id: int):
        """Create study ipdsharing metadata"""
        study_ = Study.query.get(study_id)
        if not is_granted("study_metadata", study_):
            return "Access denied, you can not delete study", 403
        study_.study_ipdsharing.update(request.json)
        db.session.commit()
        return study_.study_ipdsharing.to_dict()
