from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    email = fields.Email(required=True, validate=validate.Length(max=64))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class UserCreationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True, validate=validate.Length(min=1, max=120))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=128))

class UserUpdateSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1, max=80))
    email = fields.Email(validate=validate.Length(min=1, max=120))
    password = fields.Str(load_only=True, validate=validate.Length(min=6, max=128))

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['Pending', 'Completed', 'Canceled']))
    created_at = fields.DateTime(dump_only=True)
    items = fields.Nested('OrderItemSchema', many=True, exclude=('order',))

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    description = fields.Str(validate=validate.Length(max=512))
    price = fields.Float(required=True)
    stock = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['Pending', 'Completed', 'Failed']))
    created_at = fields.DateTime(dump_only=True)

class ReturnSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    reason = fields.Str(required=True, validate=validate.Length(max=500))
    status = fields.Str(required=True, validate=validate.OneOf(['Pending', 'Completed', 'Failed']))
    created_at = fields.DateTime(dump_only=True)
