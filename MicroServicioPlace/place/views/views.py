# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from place.models.init_db import db
from place.models.models import Lugar, LugarSchema
from flask import make_response,abort

def read_place():
    lugares = Lugar.query.order_by(Lugar.id).all()
    lugar_schema = LugarSchema(many=True)
    return lugar_schema.dump(lugares).data

def create_place(place):
    """
    This function creates a new character in the BD
    based on the passed in character data

    :param person:  character to create in BD
    :return:        201 on success, 406 on person exists
    """
    name = place.get("name")

    existing_place = (
        Lugar.query.filter(Lugar.name == name)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_place is None:

        # Create a person instance using the schema and the passed in person
        schema = LugarSchema()
        new_place = schema.load(place, session=db.session).data

        # Add the person to the database
        db.session.add(new_place)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_place).data

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "Character {0} exists already".format(name),
        )


def read_one(place_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    place = Lugar.query.get(place_id)

    # Did we find a person?
    if place is not None:

        # Serialize the data for the response
        place_schema = LugarSchema()
        data = place_schema.dump(place).data
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {place_id}")


def update(place_id, place):
    """
    This function updates an existing person in the people structure

    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_place = Lugar.query.get(place_id)

    # Did we find an existing person?
    if update_place is not None:

        # turn the passed in person into a db object
        schema = LugarSchema()
        update = schema.load(place, session=db.session).data

        # Set the id to the person we want to update
        update.id = update_place.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_place).data

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {place_id}")


def delete(place_id):
    """
    This function deletes a person from the people structure

    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    place = Lugar.query.get(place_id)

    # Did we find a person?
    if place is not None:
        db.session.delete(place)
        db.session.commit()
        return make_response(f"Person {place_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {place_id}")
