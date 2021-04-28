from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length, Range, URL, ValidationError
from django.contrib.auth import authenticate
from food.models import CustomUser


class LoginValidator(Schema):
    email = fields.Email(required=True)
    password = fields.Str(validate=[Length(5)], required=True)

    @post_load
    def auth(self, data, **kwargs):
        password = data.get("password")
        email = data.get("email")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise ValidationError(
                    "Unable to log in with provided credentials.", code="authorization"
                )
        else:
            raise ValidationError(
                "Must include 'email' and 'password'.", code="authorization"
            )
        return user


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
