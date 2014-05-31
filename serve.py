from StringIO import StringIO
from flask import Flask, g, Response, request
import os
import pandas as pd

app = Flask(__name__)

content_types = {
    'csv': 'text/csv',
    'json': 'application/json',
}

def response(frame, status=200, kind='csv'):
    return Response(
        serialize(frame, kind),
        status=status,
        mimetype=g.data_content_type,
    )

def serialize(frame, kind='csv'):
    out = StringIO()
    getattr(frame, 'to_%s' % kind)(out) # TODO: this is terrible
    out.seek(0)

    return out.read()

def data():
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

    g.data_content_type = content_types.get(fmt, 'text/plain')
    return meth(fname)

@app.route('/')
def index():
    return response(
        data(),
        kind=request.args.get('fmt', 'csv') # TODO: freakin' sanitize this!
    )

if __name__ == '__main__':
    app.run(
        debug=os.environ.get('DEBUG', '0') == '1'
    )
