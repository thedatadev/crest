from flask import jsonify

from modules.test_module import mod

@mod.route("/test", methods=['GET'])
def get():
    return jsonify(message="Hello, world! From the test module :D")