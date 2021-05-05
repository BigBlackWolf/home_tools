from django.test.testcases import TestCase, Client
from copy import deepcopy
from datetime import date

from food.models import CustomUser


class Product(TestCase):
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
        user = CustomUser.objects.create_user(
            email="test@test.com", username="test", password="tests"
        )
        user.save()
        response = self.client.post(
            "/login/", {"email": user.email, "password": "tests"}
        )
        self.token = response.data["access"]
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

    def test_get(self):
        response = self.client.get("/products/", **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": []})

    def test_post_invalid_field(self):
        test_data = deepcopy(self.test_data)
        test_data["data"]["abc"] = "aaa"

        response = self.client.post(
            "/products/",
            data=test_data,
            content_type="application/json",
            **self.headers,
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"data": {"abc": ["Unknown field."]}})

    def test_post_without_measure(self):
        test_data = deepcopy(self.test_data)
        del test_data["data"]["measure"]

        response = self.client.post(
            "/products/",
            data=test_data,
            content_type="application/json",
            **self.headers,
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
            "/products/",
            data=self.test_data,
            content_type="application/json",
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_data)

        response = self.client.get("/products/1", **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], test_data["data"][0])

        to_patch = test_data["data"][0]
        to_patch["name"] = "ttt"
        del to_patch["id"]
        del to_patch["date_modified"]
        response = self.client.patch(
            "/products/1",
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

        response = self.client.get(
            "/dishes/1", content_type="application/json", **self.headers
        )
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
                "ingredients": {},
            }
        }

        user = CustomUser.objects.create_user(
            email="test@test.com", username="test", password="tests"
        )
        user.save()
        response = self.client.post(
            "/login/", {"email": user.email, "password": "tests"}
        )
        self.token = response.data["access"]
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

    def test_get(self):
        response = self.client.get("/dishes/", **self.headers)
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

        response = self.client.get("/dishes/1", **self.headers)
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

        response = self.client.get(
            "/dishes/1", content_type="application/json", **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], {})


class Login(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data = {
            "email": "test@test.com",
            "password": "tests",
        }
        user = CustomUser.objects.create_user(
            email="test@test.com", username="test", password="tests"
        )
        user.save()
        response = self.client.post(
            "/login/", {"email": user.email, "password": "tests"}
        )
        self.token = response.data["access"]
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

    def test_fail_login(self):
        test_data = deepcopy(self.test_data)
        test_data["password"] = "12345"

        response = self.client.post(
            "/login/", test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "No active account found with the given credentials"},
        )

    def test_successful(self):
        response = self.client.post(
            "/login/", self.test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)


class Register(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_data = {
            "username": "test",
            "email": "test@test.com",
            "password": "tests",
            "password2": "tests",
        }

    def test_fail_register(self):
        test_data = deepcopy(self.test_data)
        test_data["password2"] = "qqqqq"

        response = self.client.post(
            "/register/", test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(), {"data": {"password2": ["Passwords doesn't match"]}}
        )

        response = self.client.post(
            "/register/", self.test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        test_data["password2"] = self.test_data["password"]
        test_data["username"] = "qqq"

        response = self.client.post(
            "/register/", test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {"data": {"email": ["User with current email already registered"]}},
        )

        test_data["username"] = self.test_data["username"]
        test_data["email"] = "qqq@qqq.com"

        response = self.client.post(
            "/register/", test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {"data": {"username": ["Current username is already taken"]}},
        )

    def test_successful_register(self):
        response = self.client.post(
            "/register/", self.test_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
