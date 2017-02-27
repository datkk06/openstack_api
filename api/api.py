from __future__ import print_function
import sys
import config
from common.auth import auth, token, url_join
from flask import g, Flask, jsonify, g
from flask_restful import Api, Resource
import json
import requests


app = Flask(__name__)
api = Api(app)


@app.before_request
@auth.login_required
def save_token():
    data = json.loads(g.token)
    token = data['access']['token']
    g.token_id = token['id']
    g.tenant_id = token['tenant']['id']


class test(Resource):

    def get(self):
        return jsonify(result=(g.token_id, g.tenant_id))


class flavors(Resource):

    def get(self):
        url_node = url_join(config.HOST, config.PORT_NODE, config.VER,
                            g.tenant_id, 'flavors')
        res = requests.get(url_node, headers={'Authorization': g.token_id})
        data = json.loads(res.content)
        return jsonify(result=data)

class images(Resource):

    def get(self):
        url_node = url_join(config.HOST, config.PORT_NODE, config.VER,
                            g.tenant_id, 'images')
        print (url_node, file=sys.stderr)
        res = requests.get(url_node, headers={'Authorization': g.token_id})
        data = json.loads(res.content)
        return jsonify(result=data)

api.add_resource(test, '/')
api.add_resource(flavors, '/flavors')
api.add_resource(images, '/images')
app.register_blueprint(token)
if __name__ == "__main__":
    app.run()
