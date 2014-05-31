from StringIO import StringIO
from flask import Flask, g, Response, request
import os
import pandas as pd

app = Flask(__name__)

content_types = {
    'csv': 'text/csv',
    'json': 'application/json',
}

def response(frame, status=200):
    return Response(
        serialize(frame),
        status=status,
        mimetype=g.data_content_type,
    )

def serialize(frame):
    out = StringIO()
    getattr(frame, 'to_%s' % g.data_fmt)(out)
    out.seek(0)

    return out.read()

@app.before_first_request
def load_data():
    try:
        fname = os.environ['FNAME']
    except KeyError:
        raise KeyError('FNAME must be set in the environment')

    fmt = fname.split('.')[-1]  # yes a little naive but it works most of the time

    meth = getattr(
        pd,
        'read_%s' % fmt.lower(),
        None
    )
    if meth is None:
        raise ValueError("I don't know how to read '%s' files" % fmt)

    g.data = meth(fname)
    g.data_fmt = fmt
    g.data_content_type = content_types.get(fmt, 'text/plain')

@app.route('/')
def index():
    return response(g.data)

if __name__ == '__main__':
    app.run(
        debug=os.environ.get('DEBUG', '0') == '1'
    )
