from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService


class IngredientResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'cocktails', 'ingredients'

    @classmethod
    def get_by_ingredient_id(cls, ingredient_id):
        sql = "SELECT * " \
              "FROM cocktails.ingredients " \
              "WHERE cocktails.ingredients.ingredient_id = " + ingredient_id + ";"

        res = RDBService.run_sql(sql, None, True)
        return res
