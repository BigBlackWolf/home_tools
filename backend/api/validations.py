from marshmallow import fields, Schema, post_load, post_dump
from marshmallow.validate import Length, Range, URL, ValidationError
from .models import CustomUser, Product


class RegistrationValidation(Schema):
    username = fields.Str(validate=[Length(1, 255)], required=True)
    email = fields.Email(required=True)
    password = fields.Str(validate=[Length(5)], required=True)
    password2 = fields.Str(validate=[Length(5)], required=True)

    @post_load
    def register(self, data, **kwargs):
        password = data.get("password")
        password2 = data.get("password2")
        email = data.get("email")
        username = data.get("username")

        if password2 != password:
            raise ValidationError("Passwords doesn't match", field_name="password2")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                "User with current email already registered", field_name="email"
            )
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(
                "Current username is already taken", field_name="username"
            )

        del data["password2"]
        return data


class ProductValidator(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=Length(1, 30), required=True)
    quantity = fields.Integer(
        validate=Range(
            0,
        ),
        default=0,
        required=True,
    )
    date_modified = fields.Date(dump_only=True)
    measure = fields.Integer(validate=Range(1, 3), required=True)
    category = fields.Str(validate=Length(1, 30))


class DishValidator(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(validate=Length(1, 200), required=True)
    photo = fields.Str(validate=URL())
    recipe = fields.Str(required=True)
    date_modified = fields.Date(dump_only=True)
    ingredients = fields.Dict(fields.Str, fields.Integer, required=True)
    user_id = fields.Integer(dump_only=True, required=True)

    @post_dump
    def match_ingredients(self, data, **kwargs):
        if "user_id" not in data:
            return data
        user_id = data.pop("user_id")
        ingredients = data["ingredients"]
        ingredients_presented = Product.objects.filter(
            name__in=ingredients.keys(), user=user_id
        ).values_list("name", "quantity")
        ingredients_presented = {i[0]: i[1] for i in ingredients_presented}
        for ingredient in ingredients:
            ingredients[ingredient] = {"need": ingredients[ingredient], "present": 0}
            if ingredient in ingredients_presented:
                ingredients[ingredient]["present"] = ingredients_presented[ingredient]
        return data
