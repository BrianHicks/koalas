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

@transformation
def groupby(frame, fields, **opts):
    return frame.groupby(fields, **opts)

@transformation
def sum(frame):
    return frame.sum()

@transformation
def mean(frame):
    return frame.mean()

@transformation
def median(frame):
    return frame.median()

@transformation
def resample(frame, rule, how, **opts):
    return frame.resample(rule, how, **opts)

@transformation
def localize(frame, zone):
    try:
        return frame.tz_convert(zone)
    except TypeError:
        return frame.tz_localize(zone)

@transformation
def plot(frame, **opts):
    return frame.plot(**opts)

def apply(frame, pipeline):
    for transformation in pipeline:
        name = transformation.pop('name', None)
        if name is None:
            raise KeyError('"name" key is required in transformation {!r}'.format(
                transformation
            ))

        frame = transformations[name](frame, **transformation)

    return frame
