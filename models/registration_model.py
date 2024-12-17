from marshmallow import Schema, fields, validate

class RegistrationModel(Schema):
    name = fields.Str(required=True)
    email_id = fields.Email(required=True)
    institution = fields.Str(required=True)
    sex = fields.Str(required=True, validate=validate.OneOf(['male','female']))
    number = fields.Str(required=True)
    alt_contact = fields.Str(required=True)
    qualification = fields.Str(required=True)
    experience = fields.Int(required=True)
    committee_pref = fields.List(fields.Str(required=True),validate=validate.Length(equal=3), required=True)
    portfolio_pref = fields.List(fields.List(fields.Str(),validate=validate.Length(equal=3), required=True),validate=validate.Length(equal=3), required=True)
    accommodation = fields.Str(required=False, allow_none=True)

registrationModel = RegistrationModel()