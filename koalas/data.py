import pandas as pd
from StringIO import StringIO

content_types = {
    'text/csv': (pd.read_csv, pd.DataFrame.to_csv),
    'application/json': (pd.read_json, pd.DataFrame.to_json),
    'text/html': (pd.read_html, pd.DataFrame.to_html),
}

data = None

def load(content, content_type, **options):
    global data

    try:
        func = content_types[content_type][0]
    except KeyError:
        raise KeyError(
            "I don't know how to load \"{!s}\"".format(content_type)
        )

    data = func(
        StringIO(content),
        **options
    )

def dump(content, content_type, **options):
    try:
        func = content_types[content_type][1]
    except KeyError:
        raise KeyError(
            "I don't know how to dump \"{!s}\"".format(content_type)
        )

    out = StringIO()
    func(data, out, **options)
    out.seek(0)
    return out.read()
