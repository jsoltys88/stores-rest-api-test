from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest

class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('test').save_to_db()

            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              'Found an item with a name {}, but expected not to.'.format(item.name))
            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name('test'),
                                 'Did not find an item with a name {}, but expected was to find this item.'.format(item.name))
            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name('test'),
                              'Found an item with a name {}, but expected was not to since it was deleted.'.format(item.name))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test store')