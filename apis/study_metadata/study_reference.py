from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyReference
from flask import request


from apis.study_metadata_namespace import api


study_reference = api.model(
    "StudyReference",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "type": fields.String(required=True),
        "title": fields.String(required=True),
        "citation": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/reference")
class StudyReferenceResource(Resource):
    @api.doc("reference")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_reference)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_reference_ = study_.study_reference
        print(study_.study_reference)
        sorted_study_reference = sorted(study_reference_, key=lambda x: x.created_at, reverse=True)
        return [s.to_dict() for s in sorted_study_reference]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_reference_ = StudyReference.query.get(i["id"])
                study_reference_.update(i)
                list_of_elements.append(study_reference_.to_dict())
            elif "id" not in i or not i["id"]:
                study_reference_ = StudyReference.from_data(study_obj, i)
                db.session.add(study_reference_)
                list_of_elements.append(study_reference_.to_dict())
        db.session.commit()
        return list_of_elements

    @api.route("/study/<study_id>/metadata/reference/<reference_id>")
    class StudyReferenceUpdate(Resource):
        def delete(self, study_id: int, reference_id: int):
            study_reference_ = StudyReference.query.get(reference_id)
            db.session.delete(study_reference_)
            db.session.commit()
            return 204
