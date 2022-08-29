import random

from sqlalchemy.exc import SQLAlchemyError

from app.db.database import DbSession
from app.db.tables import Rack, PDU
from app.api.response import sqlalchemy_response


def generate_obj_li(start=1, end=500):
    obj_li = []
    for i in range(start, end):
        obj_li.append(Rack(
            rack_id="rack-test-" + str(i),
            rack_height=round(random.uniform(1000, 2000),2),
            rack_location="SG-DC{}-Suite{}".format(str(random.randint(1, 10)), random.randint(1, 50))
        ))
        obj_li.append(PDU(
            pdu_id="pdu-test-" + str(i),
            pdu_capacity=round(random.uniform(1, 100),2),
            pdu_outlets_number=random.randint(1, 50)
        ))

    return {"obj_li": obj_li}


def import_mock_data(start=1, end=500):
    session = DbSession()
    object_li_mock = generate_obj_li(start, end)
    try:
        session.bulk_save_objects(object_li_mock["obj_li"])
        session.commit()
        return sqlalchemy_response.response_test(start, end)
    except SQLAlchemyError:
        session.rollback()
        return sqlalchemy_response.response_test_error(start)


if __name__ == "__main__":
    import_mock_data(1, 500)
