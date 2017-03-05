from __future__ import print_function
import sys
import config
from common.auth import auth, token, url_join
from flask import g, Flask, jsonify, g, request
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


class flavors(Resource):

    def get(self):
        url_node = url_join(config.HOST, config.PORT_NODE, config.VER_NODE,
                            g.tenant_id, 'flavors')
        print (url_node, file=sys.stderr)
        res = requests.get(url_node, headers={'X-Auth-Token': g.token_id})
        data = json.loads(res.content)
        return jsonify(data)


class images(Resource):

    def get(self, id=None):
        if not id:
            url_node = url_join(config.HOST, config.PORT_NODE, config.VER_NODE,
                                g.tenant_id, 'images')
        else:
            url_node = url_join(config.HOST, config.PORT_NODE, config.VER_NODE,
                                g.tenant_id, 'images', id)
        print (url_node, file=sys.stderr)
        res = requests.get(url_node, headers={'X-Auth-Token': g.token_id})
        data = json.loads(res.content)
        return jsonify(data)


class servers(Resource):

    def get(self, id=None):
        if not id:
            url_node = url_join(config.HOST, config.PORT_NODE, config.VER_NODE,
                                g.tenant_id, 'servers')
        else:
            url_node = url_join(config.HOST, config.PORT_NODE, config.VER_NODE,
                                g.tenant_id, 'servers', id)

        print (url_node, file=sys.stderr)
        res = requests.get(url_node, headers={'X-Auth-Token': g.token_id})
        data = json.loads(res.content)
        return jsonify(data)

    def post(self):
        url_node = url_join(config.HOST, config.PORT_NODE, config.VER_NODE,
                            g.tenant_id, 'servers')
        res = requests.post(url_node, headers={'X-Auth-Token': g.token_id},
                            json=request.get_json())
        data = json.loads(res.content)
        return jsonify(data)


api.add_resource(flavors, '/flavors')
api.add_resource(images, '/images')
api.add_resource(servers, '/servers', '/servers/<id>')
app.register_blueprint(token)
if __name__ == "__main__":
    app.run(threaded=True)
