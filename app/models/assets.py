from fastapi import Query
from pydantic import BaseModel
from enum import Enum
from typing import List, Union

from app.models.pdu import PDUModel
from app.models.racks import RacksModel


class AssetsInCreate(BaseModel):
    data: List[Union[PDUModel, RacksModel]]


class AssetsInUpdate(BaseModel):
    data: List[Union[PDUModel, RacksModel]]


class AssetsSearchOperator(BaseModel):
    field: str
    operator: str = Query(
        default=None,
        regex="^eq$|^ne$|^gt$|^lt$|^ge$|^le$|^like$|^regexp$",
    )
    value: Union[int, float, str]


class AssetsInSearch(BaseModel):
    asset_type: str = Query(
        default=None,
        regex="^rack$|^pdu$",
    )
    fields_selected: List[str] = None
    condition: List[AssetsSearchOperator] = None


class AssetPath(str, Enum):
    rack = "rack"
    pdu = "pdu"
