from StringIO import StringIO
from flask import Flask, g, Response, request
import os
import pandas as pd
from urllib import unquote_plus

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
    kind = 'csv'

    frame = data()
    columns = frame.columns
    start = 0
    end = len(frame)

    for item in request.query_string.split('&'): # TODO: again probably a little naive
        try:
            key, value = item.split('=', 1)
        except ValueError:
            continue  # but log it?

        # special cases
        if key == 'format':
            kind = value
            continue

        elif key == 'columns':
            columns = value.split(',')
            continue

        elif key == 'start':
            start = int(value)
            continue

        elif key == 'end':
            end = int(value)
            continue

        # then probably filtering!
        operators = key.split('__')
        if len(operators) == 1:
            # we're going to assume we've just got a name, and filter exactly
            # on that column. The value has to be castable to the correct
            # datatype for that column
            name = unquote_plus(operators[0])

            dtype = frame.dtypes[name].type
            values = [dtype(unquote_plus(val)) for val in value.split(',')]
            frame = frame[frame[name].isin(values)]

        else:
            name = unquote_plus(operators[0])
            dtype = frame.dtypes[name].type
            values = [dtype(unquote_plus(val)) for val in value.split(',')]

            # TODO: this process could probably be more efficient.
            mask = None
            for value in values:
                # TODO: danger danger Will Robinson! Absolutely no filtering ahead!
                inner = frame[name]
                for op in operators[1:]:
                    op_ = getattr(inner, op, None)

                    if inner is None:
                        raise AttributeError('no attribute {!r} on {!r}'.format(op, op_))
                    else:
                        if callable(op_):
                            val = op_(value)
                            break

                        elif op == 'lte':
                            val = inner < value | inner.eq(value)
                            break
                        elif op == 'gte':
                            val = inner > value | inner.eq(value)
                            break

                        else:
                            inner = op_

                if mask is None:
                    mask = val
                else:
                    mask |= val


            frame = frame[mask]

    return response(
        frame[columns][start:end],
        kind=kind # TODO: freakin' sanitize this!
    )

if __name__ == '__main__':
    app.run(
        debug=os.environ.get('DEBUG', '0') == '1'
    )
