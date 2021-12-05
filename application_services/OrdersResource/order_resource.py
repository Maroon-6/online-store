from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService
from collections import OrderedDict


class OrderResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'online_store', 'orders'

    @classmethod
    def get_by_order_id(cls, order_id):
        sql = "SELECT a.order_id, user_id, address_id, total_price, inventory_id, amount, price, status FROM " \
              "(SELECT * FROM online_store.orders where order_id = " + order_id + ") AS a " \
                                                                                  "JOIN online_store.order_details ON a.order_id = order_details.order_id;"

        sql_res = RDBService.run_sql(sql, None, True)

        if not sql_res:
            return None

        res = OrderedDict()
        res["order_id"] = sql_res[0]["order_id"]
        res["user_id"] = sql_res[0]["user_id"]
        res["address_id"] = sql_res[0]["address_id"]
        res["total_price"] = sql_res[0]["total_price"]
        res["status"] = sql_res[0]["status"]
        res["inventories"] = []

        for i in range(len(sql_res)):
            tmp = OrderedDict()
            tmp["inventory_id"] = sql_res[i]["inventory_id"]
            tmp["amount"] = sql_res[i]["amount"]
            tmp["price"] = sql_res[i]["price"]
            res["inventories"].append(tmp)

        return res

    @classmethod
    def place_order(cls, data):
        if not data:
            return False

        sql = "SELECT COUNT(order_id) as order_count FROM online_store.orders"
        sql_res = RDBService.run_sql(sql, None, True)
        order_id = sql_res[0]["order_count"] + 1

        order_info = dict()
        order_info["order_id"] = order_id
        order_info["user_id"] = data["user_id"]
        order_info["address_id"] = data["address_id"]
        order_info["total_price"] = data["total_price"]
        order_info["status"] = data["status"]

        RDBService.create("online_store", "orders", order_info)

        for inventory in data["inventories"]:
            order_detail = dict()
            order_detail["order_id"] = order_id
            order_detail["inventory_id"] = inventory["inventory_id"]
            order_detail["amount"] = inventory["amount"]
            order_detail["price"] = inventory["price"]
            RDBService.create("online_store", "order_details", order_detail)

        return True

    @classmethod
    def get_all_order_id_by_user_id(cls, user_id):
        sql = "SELECT order_id FROM online_store.orders WHERE user_id = " + user_id
        sql_res = RDBService.run_sql(sql, None, True)

        if not sql_res:
            return None

        return sql_res
