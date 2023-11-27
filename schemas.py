from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf, Range


# class TextsSchema(Schema):
#     texts = fields.List(fields.String(), required=True)

class InputSchema(Schema):
    instances = fields.List(fields.String(), required=True)

class OutputSchema(Schema):
    predictions = fields.List(fields.List(fields.String()), dump_only=True)
