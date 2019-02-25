from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    """
    This resource allows user to register by sending a
    POST request with their username and password.

    """

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        # FIRST - get the data from the parser
        data = UserRegister.parser.parse_args()


        # Search for user by username
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400  # USER with that user name already exists

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, 201
