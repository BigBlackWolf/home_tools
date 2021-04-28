from django.test.testcases import TestCase, Client
from copy import deepcopy
from datetime import date
from rest_framework.authtoken.models import Token

from food.models import CustomUser


class Food(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data = {
            "data": {
                "name": "Ogurec",
                "measure": 1,
                "quantity": 1,
                "category": "Holodilnik",
            }
        }
        user = CustomUser(email="test@test.com", username="test", password="test")
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token
        self.headers = {"HTTP_AUTHORIZATION": f"Token {token}"}

    def test_get(self):
        response = self.client.get("/food/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": []})

    def test_post_invalid_field(self):
        test_data = deepcopy(self.test_data)
        test_data["data"]["abc"] = "aaa"

        response = self.client.post(
            "/food/", data=test_data, content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"data": {"abc": ["Unknown field."]}})

    def test_post_without_measure(self):
        test_data = deepcopy(self.test_data)
        del test_data["data"]["measure"]

        response = self.client.post(
            "/food/", data=test_data, content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(), {"data": {"measure": ["Missing data for required field."]}}
        )

    def test_post_successful(self):
        test_data = deepcopy(self.test_data)
        test_data["data"]["date_modified"] = date.today().strftime("%Y-%m-%d")
        test_data["data"]["id"] = 1
        test_data["data"] = [test_data["data"]]

        response = self.client.post(
            "/food/",
            data=self.test_data,
            content_type="application/json",
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_data)

        response = self.client.get("/food/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], test_data["data"][0])

        to_patch = test_data["data"][0]
        to_patch["name"] = "ttt"
        del to_patch["id"]
        del to_patch["date_modified"]
        response = self.client.patch(
            "/food/1",
            data={"data": to_patch},
            content_type="application/json",
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["name"], "ttt")

        response = self.client.delete(
            "/dishes/1", content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], "Success")

        response = self.client.get("/dishes/1", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], {})


class Dishes(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data = {
            "data": {
                "name": "Pasta",
                "recipe": "Boil makarons",
                "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
            }
        }

        user = CustomUser(email="test@test.com", username="test", password="test")
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token
        self.headers = {"HTTP_AUTHORIZATION": f"Token {token}"}

    def test_get(self):
        response = self.client.get("/dishes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": []})

    def test_post_invalid_field(self):
        test_data = deepcopy(self.test_data)
        test_data["data"]["abc"] = "aaa"

        response = self.client.post(
            "/dishes/", data=test_data, content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"data": {"abc": ["Unknown field."]}})

    def test_post_without_name(self):
        test_data = deepcopy(self.test_data)
        del test_data["data"]["name"]

        response = self.client.post(
            "/dishes/", data=test_data, content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(), {"data": {"name": ["Missing data for required field."]}}
        )

    def test_post_successful(self):
        test_data = deepcopy(self.test_data)
        test_data["data"]["date_modified"] = date.today().strftime("%Y-%m-%d")
        test_data["data"]["id"] = 1
        test_data["data"] = [test_data["data"]]

        response = self.client.post(
            "/dishes/",
            data=self.test_data,
            content_type="application/json",
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_data)

        response = self.client.get("/dishes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], test_data["data"][0])

        to_patch = test_data["data"][0]
        to_patch["name"] = "ttt"
        del to_patch["id"]
        del to_patch["date_modified"]
        response = self.client.patch(
            "/dishes/1",
            data={"data": to_patch},
            content_type="application/json",
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["name"], "ttt")

        response = self.client.delete(
            "/dishes/1", content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], "Success")

        response = self.client.get("/dishes/1", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], {})
