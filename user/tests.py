from django.test import TestCase, TransactionTestCase
from django.urls import reverse


class UserRegistration(TransactionTestCase):
    fixtures = [
        'annotations.json',
        'frequency.json',
        'language.json',
        'user.json',
        'user_profile',
    ]

    def test_user_registration_get(self):
        """
        Test the user registration get method
        :return: pass if 403 error
        """
        response = self.client.get(reverse('user:create_user'))
        self.assertEquals(response.status_code, 403)

    def test_register_new_user(self):
        data = {
            "username": "test3",
            "password": "password",
            "first_name": "first3",
            "last_name": "last3",
            "email": "test3@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 201)

    def test_no_username_field(self):
        data = {
            # "username": "test1",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    def test_non_unique_username(self):
        data = {
            "username": "test1",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    def test_no_password_field(self):
        data = {
            "username": "test4",
            # "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    def test_no_first_language_field(self):
        data = {
            "username": "test4",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            # "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    def test_no_extra_languages(self):
        data = {
            "username": "test5",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            # "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 201)

    def test_second_language(self):
        data = {
            "username": "test6",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 201)

    def test_third_language(self):
        data = {
            "username": "test7",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 201)

    def test_wrong_first_language(self):
        data = {
            "username": "test4",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZW",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    def test_wrong_second_language(self):
        data = {
            "username": "test4",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZA",
            "third_language": "XHO-ZA",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    def test_wrong_third_language(self):
        data = {
            "username": "test4",
            "password": "password",
            "first_name": "first",
            "last_name": "last",
            "email": "test@test.com",
            "first_language": "ENG-ZA",
            "second_language": "SHO-ZW",
            "third_language": "XHO-ZW",
        }
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)


class User(TestCase):

    def test_show_this_user_details(self):
        response = self.client.get(reverse('user:user'))
        self.assertEquals(response.status_code, 403)

    def test_show_get_user_details_not_admin(self):
        # login as regular user and show details
        response = self.client.get(reverse('user:user'))
        self.assertEquals(response.status_code, 403)

    def test_show_get_user_details_admin(self):
        # login as admin and show user
        response = self.client.get(reverse('user:user'))
        self.assertEquals(response.status_code, 403)

    def test_update_user_details(self):
        data = {}
        # todo populate data object to update user
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 403)
