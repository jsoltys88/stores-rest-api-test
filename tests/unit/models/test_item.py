from unittest import TestCase
from models.item import ItemModel
from models.store import StoreModel


class ItemTest(TestCase):

    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         'Name is wrong. Please check it!') # This Third argument is to put an error message if test will not pass
        self.assertEqual(item.price, 19.99,
                         'Price is not equal. Please check it!')



    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
            }

        self.assertEqual(item.json(), expected,
                         'The JSON export of the item is incorrect. Please reverify it!')