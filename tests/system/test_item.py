import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest

class ItemTest(BaseTest):
    # set up data to be used in each test, access token is generated here in order to verify the user in every test
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app as client :
            with self.app_context() :
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username' : 'test', 'password' : '1234'}),
                                           headers={'Content-Type' : 'application/json'})
                # OUR JWT token is generated here:
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    #  TEST 1
    def test_get_item_no_auth(self):
        with self.app as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(resp.status_code, 401)


    #  TEST 2
    def test_get_item_not_found(self):
        with self.app as client:
            with self.app_context():

                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    #  TEST 3
    def test_get_item(self):
        with self.app as client :
            with self.app_context() :
                StoreModel('test').save_to_db()
                ItemModel('chair', 19.99, 1).save_to_db()

                resp = client.get('/item/test', headers={'Authorization' : self.access_token})
                self.assertEqual(resp.status_code, 404)

    #  TEST 4
    def test_delete_item(self):
        with self.app as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('chair', 19.99, 1).save_to_db()

                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(resp.data))

    #  TEST 5
    def test_create_item(self):
        with self.app as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(resp.data))

    #  TEST 6
    def test_create_duplicate_item(self):
        with self.app as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name \'test\' already exists."},
                                     json.loads(resp.data))


    # # TEST 7
    def test_put_item(self):
        with self.app as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(resp.data))


    # #  TEST 8
    def test_put_update_item(self):
        with self.app as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)

                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name' : 'test', 'price' : 17.99},
                                     json.loads(resp.data))


    # #  TEST 9
    def test_item_list(self):
        with self.app as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 19.99}]},
                                     json.loads(resp.data))
