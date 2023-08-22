from model import Study

from flask_restx import Namespace, Resource, fields


api = Namespace("identification", description="study operations", path="/")


study_identification = api.model(
    "StudyIdentification",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.Boolean(required=True),
        "identifier_domain": fields.String(required=True),
        "identifier_link": fields.String(required=True),
        "secondary": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/identification")
class StudyArmResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    # @api.marshal_with(study_identification)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_identification_ = study_.study_identification
        return [s.to_dict() for s in study_identification_]

