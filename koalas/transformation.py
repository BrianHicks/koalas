transformations = {}

def transformation(func):
    global transformations
    transformations[func.__name__] = func

    return func

@transformation
def select(frame, fields):
    if not isinstance(fields, list):
        raise ValueError('"fields" must be a list')

    return frame[fields]

@transformation
def slice(frame, lower=0, upper=None, step=1):
    return frame[lower:upper or len(frame):step]

@transformation
def lt(frame, field, value):
    return frame[frame[field] < value]

@transformation
def lte(frame, field, value):
    return frame[frame[field] <= value]

@transformation
def gt(frame, field, value):
    return frame[frame[field] > value]

@transformation
def gte(frame, field, value):
    return frame[frame[field] >= value]

@transformation
def eq(frame, field, value):
    return frame[frame[field] == value]

@transformation
def ne(frame, field, value):
    return frame[frame[field] != value]

def apply(frame, pipeline):
    for transformation in pipeline:
        name = transformation.pop('name', None)
        if name is None:
            raise KeyError('"name" key is required in transformation {!r}'.format(
                transformation
            ))

        frame = transformations[name](frame, **transformation)

    return frame
