from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf, Range


class InputSchema(Schema):
    texts = fields.List(fields.String(), required=True)

class OutputSchema(Schema):
    locations = fields.List(fields.List(fields.String()), dump_only=True)
