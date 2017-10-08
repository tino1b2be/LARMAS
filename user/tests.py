from django.test import TestCase
from django.urls import reverse


class UserRegistration(TestCase):

    def test_user_registration_get(self):
        """
        Test the user registration get method
        :return: pass if 403 error
        """
        response = self.client.get(reverse('user:create_user'))
        self.assertEquals(response.status_code, 403)

    def test_register_new_user(self):
        data = {}
        # todo populate data object to register new user
        response = self.client.post(reverse('user:create_user'), data)
        self.assertEquals(response.status_code, 400)

    # todo implement test
    def test_no_username_field(self):
        pass

    def test_non_unique_username(self):
        pass

    def test_no_password_field(self):
        pass

    def test_no_first_language_field(self):
        pass

    def test_no_extra_languages(self):
        pass

    def test_second_language(self):
        pass

    def test_third_language(self):
        pass

    def test_wrong_first_language(self):
        pass

    def test_wrong_second_language(self):
        pass


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
