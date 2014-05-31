def select(frame, fields):
    if not isinstance(fields, list):
        raise ValueError('"fields" must be a list')

    return frame[fields]

def lt(frame, field, value):
    return frame[frame[field] < value]

def lte(frame, field, value):
    return frame[frame[field] <= value]

def gt(frame, field, value):
    return frame[frame[field] > value]

def gte(frame, field, value):
    return frame[frame[field] >= value]

def eq(frame, field, value):
    return frame[frame[field] == value]

def ne(frame, field, value):
    return frame[frame[field] != value]

def transform(frame, pipeline):
    for transformation in pipeline:
        name = transformation.pop('name', None)
        if name is None:
            raise KeyError('"name" key is required in transformation {!r}'.format(
                transformation
            ))

        frame = transformations[name](frame, **transformation)

    return frame
