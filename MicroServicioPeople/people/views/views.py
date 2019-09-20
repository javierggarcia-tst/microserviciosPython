# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from people.models.init_db import db
from people.models.models import Personaje, PersonajeSchema
from flask import make_response,abort

def read_characters():
    personajes = Personaje.query.order_by(Personaje.id).all()
    person_schema = PersonajeSchema(many=True)
    return person_schema.dump(personajes).data

def create_character(character):
    """
    This function creates a new character in the BD
    based on the passed in character data

    :param person:  character to create in BD
    :return:        201 on success, 406 on person exists
    """
    isAlive = character.get("isAlive")
    name = character.get("name")
    placeId = character.get("placeId")

    existing_character = (
        Personaje.query.filter(Personaje.name == name)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_character is None:

        # Create a person instance using the schema and the passed in person
        schema = PersonajeSchema()
        new_person = schema.load(character, session=db.session).data

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person).data

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "Character {0} exists already".format(name),
        )


def read_one(character_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    personaje = Personaje.query.get(character_id)

    # Did we find a person?
    if personaje is not None:

        # Serialize the data for the response
        person_schema = PersonajeSchema()
        data = person_schema.dump(personaje).data
        print(type(data))
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {character_id}")


def update(character_id, character):
    """
    This function updates an existing person in the people structure

    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_person = Personaje.query.get(character_id)

    # Did we find an existing person?
    if update_person is not None:

        # turn the passed in person into a db object
        schema = PersonajeSchema()
        update = schema.load(character, session=db.session).data

        # Set the id to the person we want to update
        update.id = update_person.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_person).data

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {character_id}")


def delete(character_id):
    """
    This function deletes a person from the people structure

    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Personaje.query.get(character_id)

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(f"Person {character_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {character_id}")
