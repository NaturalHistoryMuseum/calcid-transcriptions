import json
import decimal
# from sqlalchemy.ext.declarative import DeclarativeMeta


class Encoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, decimal.Decimal):
            return str(o)

        return super(Encoder, self).default(o)
