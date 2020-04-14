from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse
import redis, json

app = Flask(__name__)
api = Api(app, version='1.0', title='Board API',
    description='A simple board API',
)

# -----------------------------------------------------
# Redis DB 설정
# -----------------------------------------------------
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

# -----------------------------------------------------
# Restplus 패키지 설정
# -----------------------------------------------------
ps = api.namespace('boards', description='Boarding operations')

board = api.model('Board', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(requierd=True, description='The title of post'),
    'content': fields.String(required=True, description='The post details')
})

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)

# -----------------------------------------------------
# DAO 설정
# -----------------------------------------------------
class BoardDAO(object):
    def __init__(self):
        self.counter = 0

    def get(self, id):
        r.get(id)
        if board is 0:
            api.abort(404, "Board {} doesn't exist".format(id))
        else:
            return json.loads(r.get(id))

    def get_all(self):
        boards = []
        for board in r.scan_iter():
            boards.append(json.loads(r.get(board)))
        return boards

    def create(self):
        args = parser.parse_args()
        args['id'] = self.counter = self.counter + 1
        r.set(self.counter, json.dumps(args))
        return args

    def update(self, id):
        args = parser.parse_args()
        args['id'] = id
        r.set(id, json.dumps(args))
        return args

    def delete(self, id):
        r.delete(id)

DAO = BoardDAO()


# -----------------------------------------------------
# URL 매핑
# -----------------------------------------------------
@ps.route('/')
class BoardList(Resource):
    '''Shows a list of all boards, and lets you post to add new boards'''
    @ps.doc('list_boards')
    @ps.marshal_list_with(board)
    def get(self):
        '''List all boards'''
        return DAO.get_all(), 200

    @ps.doc('create_post')
    @ps.expect(parser)
    @ps.marshal_with(board, code=200)
    def post(self):
        '''Create a new board'''
        return DAO.create(), 200


@ps.route('/<int:id>')
@ps.response(404, 'Board not found')
@ps.param('id', 'The board identifier')
class Todo(Resource):
    '''Show a single board item and lets you delete them'''
    @ps.doc('get_board')
    @ps.marshal_list_with(board)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id), 200

    @ps.doc('delete_board')
    @ps.response(200, 'board deleted')
    def delete(self, id):
        '''Delete a board given its identifier'''
        DAO.delete(id)
        return '', 200

    @ps.expect(parser)
    @ps.marshal_with(board)
    def put(self, id):
        '''Update a board given its identifier'''
        return DAO.update(id), 200


if __name__ == '__main__':
    app.run(debug=True)