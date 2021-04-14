from marshmallow import fields, Schema
from marshmallow.validate import Length, Range, URL


class ProductValidator(Schema):
    name = fields.Str(validate=Length(1, 30))
    quantity = fields.Integer(validate=Range(0, ))
    date_modified = fields.Date(dump_only=True)
    measure = fields.Integer(validate=Range(1, 3))
    category = fields.Str(validate=Length(1, 30))


class DishValidator(Schema):
    name = fields.Str(max_length=30, unique=True, blank=False)
    photo = fields.Str(validate=URL())
    recipe = fields.Str()
    date_modified = fields.Date(dump_only=True)
    ingredients = fields.Dict(fields.Str, fields.Integer)
