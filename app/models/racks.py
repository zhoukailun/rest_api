from fastapi import Query
from pydantic import BaseModel
from typing import Optional


class RacksModel(BaseModel):
    asset_type: str = Query(regex="^rack$")
    rack_id: str = Query(min_length=1, max_length=32)
    rack_height: Optional[float] = 0
    rack_location: Optional[str] = Query(default="", max_length=50)

    def to_json(self):
        """
        convert object to json/dict type
        :return: dict
        """
        if not self.rack_height:
            self.rack_height = 0
        json_dict = {
            "rack_id": self.rack_id,
            "rack_height": float(self.rack_height),
            "rack_location": self.rack_location
        }
        return json_dict