# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from juegoTornos.models.models import JuegoTornos, JuegoPeople
from flask import make_response,abort
import requests
import json

def read_all():
    respPlace = requests.get('http://desktop-638bfha:8082/place/places')
    respPeople = requests.get('http://desktop-638bfha:8081/people/people')
    arrayPlaces = []

    jsonPlaces = respPlace.json()
    jsonPeoples = respPeople.json()

    if len(jsonPlaces) > 0:
        for place in jsonPlaces:
            kk = dict()
            kk["id"] = place["id"]
            kk["name"] = place["name"]
            kk["people"] = []
            for people in jsonPeoples:
               if people["placeId"] == kk["id"] and people["isAlive"] == True:
                   pp = dict()
                   pp["id"] = people["id"]
                   pp["name"] = people["name"]
                   pp["isAlive"] = people["isAlive"]
                   kk["people"].append(pp)
            arrayPlaces.append(kk)
        return arrayPlaces, 200
    else:
        abort(404, "No places")

def read_one(juego_id):
    """
    This function responds to a request for /api/juegotornos/{juego_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    respPlace = requests.get('http://desktop-638bfha:8082/place/places/'+str(juego_id))
    respPeople = requests.get('http://desktop-638bfha:8081/people/people')
           
    jsonPlaces = respPlace.json()
    jsonPeoples = respPeople.json()
    
    if len(jsonPlaces) > 0:
        placeResponse = dict()
        placeResponse["id"] = jsonPlaces["id"]
        placeResponse["name"] = jsonPlaces["name"]
        placeResponse["people"] = []
        for people in jsonPeoples:
            if people["placeId"] == placeResponse["id"] and people["isAlive"] == True:
                pp = dict()
                pp["id"] = people["id"]
                pp["name"] = people["name"]
                pp["isAlive"] = people["isAlive"]
                placeResponse["people"].append(pp)
        
        return placeResponse, 200
    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {juego_id}")
