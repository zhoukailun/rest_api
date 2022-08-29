from sqlalchemy.exc import SQLAlchemyError

from app.db.tables import Rack, PDU
from app.db.database import DbSession
from app.api.response import sqlalchemy_response


class DBOperator:
    def __init__(self):
        self.session = DbSession()

    def create(self, objects_li):
        """
        create objects to sqlite db
        :param objects_li: list of objects to add
        :return: JSONResponse
        """
        if not objects_li:
            return sqlalchemy_response.response_empty_data()

        # generate object adding list
        obj_operation_li = []
        for obj in objects_li:
            if obj.asset_type == "rack":
                obj_operation_li.append(Rack(
                    rack_id=obj.rack_id,
                    rack_height=obj.rack_height,
                    rack_location=obj.rack_location)
                )
            elif obj.asset_type == "pdu":
                obj_operation_li.append(PDU(
                    pdu_id=obj.pdu_id,
                    pdu_capacity=obj.pdu_capacity,
                    pdu_outlets_number=obj.pdu_outlets_number)
                )
            else:
                return sqlalchemy_response.response_error_asset_type()
        # add objects if no error
        try:
            self.session.bulk_save_objects(obj_operation_li)
            self.session.commit()
            return sqlalchemy_response.response_create(len(obj_operation_li))
        except SQLAlchemyError as e:
            self.session.rollback()
            return sqlalchemy_response.response_error(e)

    def search_by_id(self, asset_type, id):
        """
        search objects from sqlite db by asset id, eg rack_id, pdu_id
        :param asset_type: asset type, eg. rack, pdu
        :param id: asset id, eg. rack_id, pdu_id
        :return: JSONResponse
        """
        if asset_type == "rack":
            ObjSearch = Rack
        elif asset_type == "pdu":
            ObjSearch = PDU
        else:
            return sqlalchemy_response.response_search_error(
                "Unkown asset_type '{}'".format(asset_type)
            )

        try:
            sql_query_obj = self.session.query(ObjSearch).filter(getattr(ObjSearch, asset_type + "_id") == id)
            result_query = sql_query_obj.all()
        except SQLAlchemyError as e:
            return sqlalchemy_response.response_search_error(e)

        response_data = []
        for obj in result_query:
            response_data.append(obj.to_json())
        return sqlalchemy_response.response_search(len(response_data), response_data)

    def search(self, condition_dict):
        """
         search objects from sqlite db by queries
         :param condition_dict: query conditions
         :return: JSONResponse which contains data
         """
        asset_type = condition_dict.asset_type
        if asset_type == "rack":
            ObjSearch = Rack
        elif asset_type == "pdu":
            ObjSearch = PDU
        else:
            return sqlalchemy_response.response_search_error(
                "Unkown asset_type '{}'".format(asset_type)
            )
        # query for multiple conditions
        try:
            sql_query_obj = self.session.query(ObjSearch)
            for cond in condition_dict.condition:
                filter_cond = self.search_operator_transform(cond.operator, getattr(ObjSearch, cond.field), cond.value)
                sql_query_obj = sql_query_obj.filter(filter_cond)

            result_query = sql_query_obj.all()
        except SQLAlchemyError as e:
            return sqlalchemy_response.response_search_error(e)
        except AttributeError:
            return sqlalchemy_response.response_error_attribute()


        # append all fields if 'fields_selected' was empty, otherwise append selected fields
        response_data = []
        if not condition_dict.fields_selected:
            for obj in result_query:
                response_data.append(obj.to_json())
        else:
            for obj in result_query:
                obj_json = obj.to_json()
                obj_data = {}
                for field in condition_dict.fields_selected:
                    obj_data[field] = obj_json.get(field)
                response_data.append(obj_data)
        return sqlalchemy_response.response_search(len(response_data), response_data)

    def update(self, objects_li):
        """
        search objects by asset id and update objects attributes in sqlite db
        :param objects_li: object list to be updated
        :return: JSONResponse
        """
        # search id and update for each object
        count_succ = 0
        for obj in objects_li:
            asset_type = obj.asset_type
            if asset_type == "rack":
                ObjUpdate = Rack
            elif asset_type == "pdu":
                ObjUpdate = PDU
            else:
                return sqlalchemy_response.response_update_error(
                    count_succ,
                    "Unkown asset_type '{}'".format(asset_type)
                )

            # search accorindg to asset id
            result_search = self.session.query(ObjUpdate)\
                .filter(getattr(ObjUpdate, asset_type + "_id") == getattr(obj, asset_type + "_id"))
            if not result_search.all():
                return sqlalchemy_response.response_update_error(
                    count_succ,
                    "No matching data found for {}_id '{}'".format(asset_type, getattr(obj, asset_type + "_id"))
                )

            # generate update data for each object
            update_data = {}
            obj_json = obj.to_json()
            for attr, val in obj_json.items():
                if attr == "asset_type" or attr == asset_type + "_id":
                    continue
                update_data[getattr(ObjUpdate, attr)] = val

            # update if no error, count
            try:
                result_search.update(update_data, synchronize_session=False)
                self.session.commit()
                count_succ += 1
            except SQLAlchemyError as e:
                self.session.rollback()
                return sqlalchemy_response.response_update_error(
                    count_succ,
                    "{}_id '{}'".format(asset_type, getattr(obj, asset_type + "_id")) + str(e)
                )
        return sqlalchemy_response.response_update(len(objects_li))

    @staticmethod
    def search_operator_transform(operator, Obj, val):
        """
        transform string operators to python operator
        :param operator: string operators
        :param Obj: Asset object
        :param val: values after the operator
        :return: Asset object filter expression
        """
        if operator == "eq":
            return Obj == val
        if operator == "ne":
            return Obj != val
        if operator == "gt":
            return Obj > val
        if operator == "lt":
            return Obj < val
        if operator == "ge":
            return Obj >= val
        if operator == "le":
            return Obj <= val
        if operator == "like":
            return Obj.like(val)
        if operator == "regexp":
            return Obj.op("regexp")(val)
        return
