# lib/required.py

from marshmallow import Schema, fields, ValidationError
from pprint import pprint

# schema

class HamsterSchema(Schema):
     name = fields.Str(required=True)
     breed = fields.Str()

hamster_data = [
    {"name": "Hammy", "breed": "Syrian"},   # valid
    {"name": "Wiggles"},                    # valid, breed is not required
    {"breed": "Winter White"},              # invalid, name is required
    {}                                      # invalid, name is required
]

try:
    HamsterSchema(many=True).load(hamster_data)

except ValidationError as err:
    print("Valid data:")
    pprint(err.valid_data)
    # => [{'breed': 'Syrian', 'name': 'Hammy'},
    # => {'name': 'Wiggles'},
    # => {'breed': 'Winter White'},
    # => {}]
    print("Invalid data:")
    pprint(err.messages)
    # => {2: {'name': ['Missing data for required field.']},
    # => 3: {'name': ['Missing data for required field.']}}