from __future__ import annotations
from uuid import uuid4

from app.crud.base import CRUDBase
from app.models import Response, Node, Group, User
from app.schemas import ResponseCreate, ResponseUpdate, Response as ResponseOut
from app.schema_types import NodeType
from .crud_files import files


class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate, ResponseOut]):
    def get_from_node(self, *, node: Node, group: Group | None = None, user: User | None = None) -> Response | None:
        if group:
            return group.responses.filter((Response.group_id == group.id) & (Response.node_id == node.id)).first()
        if user:
            return user.responses.filter((Response.respondent_id == user.id) & (Response.node_id == node.id)).first()
        return None

    def get_formatted_response(self, *, db_obj: Node, user: User = None) -> ResponseOut | None:
        if user:
            db_obj = self.get_from_node(node=db_obj, user=user)
            if db_obj:
                return self.get_schema(db_obj=db_obj)
        elif db_obj.formType not in [NodeType.VALUE, NodeType.VALUERANGE, NodeType.UPLOAD]:
            response_objs = db_obj.responses.all()
            if response_objs:
                obj_in = {}
                for response in response_objs:
                    if response.answer:
                        answer = {**response.answer}
                        obj_in[answer["id"]] = obj_in.get(answer["id"], answer)
                        obj_in[answer["id"]]["count"] = obj_in[answer["id"]].get("count", 0) + 1
                if obj_in:
                    # Neither of `id` or `respondent_id` matter here
                    return ResponseOut(
                        **{
                            "id": str(uuid4()),
                            "answer": obj_in,
                            "language": db_obj.language,
                            "node_id": db_obj.id,
                            "respondent_id": str(uuid4()),
                        }
                    )
        return None

    ###################################################################################################
    # RESPONSE VALIDATION
    ###################################################################################################

    def validate(self, *, node: Node, response: ResponseCreate) -> bool:
        validationResponse = {
            "VALUE": self.validateValue,
            "VALUERANGE": self.validateValueRange,
            "SCALE": self.validateScale,
            "BOOLEAN": self.validateBoolean,
            "SELECTONE": self.validateSelectOne,
            "SELECTMANY": self.validateSelectMany,
            "SELECTBRANCH": self.validateSelectOne,
            "UPLOAD": self.validateUpload,
        }
        try:
            if validationResponse[node.formType.value](node=node, response=response):
                return True
            return False
        except Exception:
            return False

    def _has_term(self, *, node: Node, term_id: str) -> bool:
        # language doesn't matter since all the IDs match
        if node.form[node.language].form and node.form[node.language].form.get("terms", []):
            return next(
                (True for term in node.form[node.language].form.get("terms", []) if term["id"] == term_id), False
            )
        return False

    def _within_limit(self, *, node: Node, limit: int) -> int | bool:
        if node.form[node.language].form and node.form[node.language].form.get("constraints", {}):
            node_limit = node.form[node.language].form.get("constraints", {}).get("limit", False)
            return not node_limit or node_limit >= limit
        return True

    def _within_min_max(self, *, node: Node, minimum: float | None = None, maximum: float | None = None) -> bool:
        if minimum and maximum and minimum > maximum:
            return False
        if (
            node.form[node.language].form
            and node.form[node.language].form.get("constraints", {})
            and any([node.form[node.language].form.get("constraints", {}).get(m) for m in ["minimum", "maximum"]])
        ):
            if node.form[node.language].form.get("constraints", {}).get("minimum") and any(
                [float(node.form[node.language].form["constraints"]["minimum"]) > m for m in [minimum, maximum] if m]
            ):
                return False
            if node.form[node.language].form.get("constraints", {}).get("maximum") and any(
                [float(node.form[node.language].form["constraints"]["maximum"]) < m for m in [minimum, maximum] if m]
            ):
                return False
        return True

    def _of_stringtype(self, *, node: Node) -> bool:
        return node.form[node.language].form.get("formType") and node.form[node.language].form.get("formType") not in [
            "NUMBER",
            "INTEGER",
            "YEAR",
        ]

    def validateSelectOne(self, *, node: Node, response: ResponseCreate) -> bool:
        return (
            isinstance(response.answer.terms, dict)
            and response.answer.terms.get("id")
            and self._has_term(node=node, term_id=response.answer.terms.get("id"))
        )

    def validateSelectMany(self, *, node: Node, response: ResponseCreate) -> bool:
        # terms arrive as {'0': answer, '1': answer, ...}
        answerList = []
        if response.answer.terms:
            answerList = list(response.answer.terms.values())
        return (
            isinstance(answerList, list)
            and all([isinstance(r, dict) for r in answerList])
            and all([r.get("id") for r in answerList])
            and all([self._has_term(node=node, term_id=r.get("id")) for r in answerList])
            and self._within_limit(node=node, limit=len(answerList))
        )

    def validateValue(self, *, node: Node, response: ResponseCreate) -> bool:
        return (
            isinstance(response.answer.terms, dict)
            and response.answer.terms.get("id")
            and (
                self._of_stringtype(node=node)
                or self._within_min_max(node=node, minimum=float(response.answer.terms.get("value")))
            )
        )

    def validateValueRange(self, *, node: Node, response: ResponseCreate) -> bool:
        answerList = []
        if response.answer.terms:
            answerList = list(response.answer.terms.values())
        return (
            isinstance(answerList, list)
            and len(answerList) == 2
            and all([isinstance(r, dict) for r in answerList])
            and all([r.get("id") for r in answerList])
            and all([self._has_term(node=node, term_id=r.get("id")) for r in answerList])
            and self._within_min_max(
                node=node, minimum=float(answerList[0].get("value")), maximum=float(answerList[1].get("value"))
            )
        )

    def validateScale(self, *, node: Node, response: ResponseCreate) -> bool:
        # node.form.terms provide min max values
        scaleMin = int(node.form[node.language].form["terms"][0]["value"])
        scaleMax = int(node.form[node.language].form["terms"][1]["value"])
        return (
            isinstance(response.answer.terms, dict)
            and response.answer.terms.get("value")
            and isinstance(int(response.answer.terms["value"]), int)
            and int(response.answer.terms["value"]) >= scaleMin
            and int(response.answer.terms["value"]) <= scaleMax
        )

    def validateBoolean(self, *, node: Node, response: ResponseCreate) -> bool:
        return (
            isinstance(response.answer.terms, dict)
            and response.answer.terms.get("id")
            and response.answer.terms["id"] in ["TRUE", "FALSE"]
        )

    def validateUpload(self, *, node: Node, response: ResponseCreate) -> bool:
        return (
            isinstance(response.answer.terms, dict)
            and response.answer.terms.get("id")
            and files.exists(folder_id=node.id, source_id=response.answer.terms["id"])
        )


response = CRUDResponse(model=Response, schema=ResponseOut)
