from marshmallow import fields, Schema
from marshmallow.validate import Length, Range, URL


class ProductValidator(Schema):
    name = fields.Str(validate=Length(1, 30), required=True)
    quantity = fields.Integer(
        validate=Range(
            0,
        ),
        required=True,
    )
    date_modified = fields.Date(dump_only=True)
    measure = fields.Integer(validate=Range(1, 3), required=True)
    category = fields.Str(validate=Length(1, 30))


class DishValidator(Schema):
    name = fields.Str(validate=Length(1, 200), required=True)
    photo = fields.Str(validate=URL())
    recipe = fields.Str(required=True)
    date_modified = fields.Date(dump_only=True)
    ingredients = fields.Dict(fields.Str, fields.Integer)
