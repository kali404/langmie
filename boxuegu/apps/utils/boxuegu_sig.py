from itsdangerous import TimedJSONWebSignatureSerializer as Slizer
from django.conf import settings


def dumps(json, expires):
    slizer = Slizer(settings.SECRET_KEY, expires)
    token = slizer.dumps(json)
    return token.decode()


def loads(s, expires):
    slizer = Slizer(settings.SECRET_KEY, expires)
    try:
        jsons = slizer.loads(s)
    except:
        return None
    else:
        return jsons
