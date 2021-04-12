from marshmallow import fields, Schema
from marshmallow.validate import Length, Range


class ProductValidator(Schema):
    name = fields.Str(validate=Length(1, 30), required=True)
    quantity = fields.Integer(validate=Range(0, ))
    date_modified = fields.Date(dump_only=True)
    measure = fields.Integer(validate=Range(1, 3))
    category = fields.Str(validate=Length(1, 30))
