import json
import os
import unittest
from typing import Dict, List, Union, Text

from people.app import MicroservicePeople
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT


def _format_response(response: Text = "") -> Union[List, Dict]:
    # python3.5 compatibility
    if isinstance(response, bytes):
        response = str(response, encoding="utf-8")
    return json.loads(response)


class PeopleTestCase(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    id_creacion = 0

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")
        ms = MicroservicePeople(service="ms", path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "people", "test_views.py"))
        self.app = ms.create_app()
        self.base_url = self.app.config["APPLICATION_ROOT"]
        self.client = self.app.test_client()

    def tearDown(self):
        pass # os.unlink(self.app.config['DATABASE'])

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(404, response.status_code)

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(200, response.status_code)

    def test_list_view(self):
        response = self.client.get('{base_url}/people'.format(base_url=self.base_url))
        self.assertEqual(200, response.status_code)

    def test_create_view(self):
        name = "nombreTest1"
        isAlive = True
        placeId = 2
        response = self.client.post('{base_url}/people'.format(
            base_url=self.base_url),
            data=json.dumps(dict(name=name,isAlive=isAlive,placeId=placeId)),
            content_type='application/json'
        )
        self.id_creacion = _format_response(response.data)["id"]
        self.assertEqual(201, response.status_code)
        self.assertEqual(name, _format_response(response.data)["name"])

    def test_create_view2(self):
        name = "nombreTest2"
        isAlive = False
        response = self.client.post('{base_url}/people'.format(
            base_url=self.base_url),
            data=json.dumps(dict(name=name,isAlive=isAlive)),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(name, _format_response(response.data)["name"])

    def test_create_view_failExist(self):
        name = "nombreTest1"
        isAlive = True
        placeId = 2
        response = self.client.post('{base_url}/people'.format(
            base_url=self.base_url),
            data=json.dumps(dict(name=name,isAlive=isAlive,placeId=placeId)),
            content_type='application/json'
        )
        self.assertEqual(409, response.status_code)

    def test_create_view_failInput(self):
        isAlive = True
        placeId = 1
        response = self.client.post('{base_url}/people'.format(
            base_url=self.base_url),
            data=json.dumps(dict(isAlive=isAlive,placeId=placeId)),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

    def test_getOne_view(self):
      response = self.client.get('{base_url}/people/1'.format(base_url=self.base_url))
      self.assertEqual(200, response.status_code)
      self.assertEqual(1,_format_response(response.data)["id"])
      self.assertEqual("Sensei Lamister",_format_response(response.data)["name"])

    def test_update_view(self):
        character_id = 27
        name = "Nombrecico44"
        isAlive = True
        placeId = 2

        response = self.client.put('{base_url}/people/27'.format(
            base_url=self.base_url),
            data=json.dumps(dict(name=name,isAlive=isAlive,placeId=placeId)),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(name, _format_response(response.data)["name"])
        self.assertEqual(character_id, _format_response(response.data)["id"])
        self.assertEqual(isAlive, _format_response(response.data)["isAlive"])
        self.assertEqual(placeId, _format_response(response.data)["placeId"])

    def test_delete_view(self):
        response = self.client.delete('{base_url}/people/59'.format(base_url=self.base_url))
        self.assertEqual(200, response.status_code)
