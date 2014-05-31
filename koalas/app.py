from flask import Flask, request, jsonify
from . import data
from . import transformation

app = Flask(__name__)

@app.route('/dataframe', methods=['POST'])
def load():
    try:
        content = request.headers['Content-Type']
    except KeyError:
        return jsonify({'details': 'Content-Type header is required'}), 400

    try:
        data.load(request.data, content, **request.args)
    except KeyError as err:
        return jsonify({'details': err.message}), 400

    return jsonify({'details': 'loaded {} rows'.format(len(data.data))}), 201


@app.route('/query', methods=['POST'])
def query():
    frame = data.data

    try:
        frame = transformation.apply(frame, request.json)
    except (KeyError, TypeError) as err:
        return jsonify({'details': err.message}), 400

    try:
        return data.dump(
            frame,
            request.headers['Accept'],
            **request.args
        )
    except KeyError as err:
        return jsonify({'details': err.message}), 400
