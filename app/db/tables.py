from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.db.database import Base


class Rack(Base):
    __tablename__ = "rack"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rack_id = Column(String(32), unique=True, nullable=False)
    rack_height = Column(Float(16, 2))
    rack_location = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)

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
            "rack_location": self.rack_location,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
        return json_dict


class PDU(Base):
    __tablename__ = "pdu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pdu_id = Column(String(32), unique=True, nullable=False)
    pdu_capacity = Column(Float(16, 2))
    pdu_outlets_number = Column(Integer)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)

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
            "pdu_outlets_number": self.pdu_outlets_number,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
        return json_dict
