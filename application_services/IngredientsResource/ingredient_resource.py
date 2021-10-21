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
        return 'cocktails', 'recipes'

    @classmethod
    def get_by_ingredient_id(cls, ingredient_id):
        sql = "SELECT ingredient_name, inventory_name, brand, quantity, price, stock" \
              "FROM cocktails.ingredients, cocktails.inventories" \
              "WHERE cocktails.ingredients.ingredient_id = " + ingredient_id + \
              "cocktails.ingredients.ingredient_id = ocktails.inventories.ingredient.id"

        res = RDBService.run_sql(sql, None, True)
        return res
