# lib/builtin.py

from marshmallow import Schema, fields, validate, ValidationError
from pprint import pprint

class VetSchema(Schema):

    name = fields.Str(validate=lambda str: str.startswith("Dr."))
    email = fields.Email()   #Email has built-in validation
    website = fields.URL()   #URL has built-in validation
    specialty = fields.Str(validate=validate.Length(min=1))
    years_practice = fields.Int(validate=validate.Range(min=0, max=100),  )
    diploma = fields.Str(validate=validate.OneOf(["DVM", "VMD"]))

# field-level validation

vet_data = [
    {"name": "Dr. Wags", "email": "email.com"},                                     # invalid email
    {"name": "Dr. Wags", "email": "wags@email.com",  "website": "htp:company.com"}, # invalid URL
    {"name": "Dr. Wags", "email": "wags@email.com",  "specialty": ""} ,             # invalid specialty
    {"name": "Dr. Wags", "email": "wags@email.com",  "years_practice": -5},         # invalid years of practice
    {"name": "Dr. Wags", "email": "wags@email.com", "diploma": "none"},             # invalid diploma
    {"name": "Mr. Wags", "email": "wags@email.com"},                                # invalid name
]

try:
    result = VetSchema(many=True).load(vet_data)
    pprint(result)
except ValidationError as err:
    pprint(err.messages)
    # => 0: {'email': ['Not a valid email address.']},
    # => 1: {'website': ['Not a valid URL.']},
    # => 2: {'specialty': ['Shorter than minimum length 1.']},
    # => 3: {'years_practice': ['Must be greater than or equal to 0 and less than or equal to 100.']}},
    # => 4: {'diploma': ['Must be one of: DVM, VMD.']}},
    # => 5: {'name': ['Invalid value.']}}