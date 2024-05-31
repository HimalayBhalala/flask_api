from marshmallow import Schema,fields

class UserSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    created = fields.DateTime()