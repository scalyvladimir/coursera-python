import json
import functools


def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = json.dumps(func(*args, **kwargs))
        return result

    return wrapped


@to_json
def get_data():
    return {
        'data': 42
    }

test = to_json(get_data)

print(test())