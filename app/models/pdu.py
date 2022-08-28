from fastapi import Query
from pydantic import BaseModel
from typing import Optional


class PDUModel(BaseModel):
    asset_type: str = Query(regex="^pdu$")
    pdu_id: str = Query(min_length=1, max_length=32)
    pdu_capacity: Optional[float] = 0
    pdu_outlets_number: Optional[int] = 0

    def to_json(self):
        """
        convert object to json/dict type
        :return: dict
        """
        if not self.pdu_capacity:
            self.pdu_capacity = 0
        json_dict = {
            "pdu_id": self.pdu_id,
            "pdu_capacity": float(self.pdu_capacity),
            "pdu_outlets_number": self.pdu_outlets_number
        }
        return json_dict
