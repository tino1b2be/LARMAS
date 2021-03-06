from django.test import TestCase, TransactionTestCase
from django.urls import reverse


class UserRegistration(TransactionTestCase):
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
    ]

    def test_register_new_user(self):
        data = {
            "username": "test3",
            "password": "password",
            "first_name": "first3",
            "last_name": "last3",
            "age": 18,
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
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
    ]

    def test_show_this_user_details(self):
        if not self.client.login(username='test2', password='password'):
            self.fail('User could not login.')
        response = self.client.get(reverse('user:user'))
        self.assertEquals(response.status_code, 200)
        f = response.data['user']['first_name']
        l = response.data['user']['last_name']
        e = response.data['user']['email']
        lang1 = response.data['first_language'].upper()
        lang2 = response.data['second_language'].upper()
        lang3 = response.data['third_language'].upper()
        self.assertEqual(lang1, 'ENGLISH')
        self.assertEqual(lang2, 'ISIZULU')
        self.assertEqual(lang3, 'SOUTH_AFRICAN_SIGN_LANGUAGE')
        self.assertEqual(f, 'first2')
        self.assertEqual(l, 'last2')
        self.assertEqual(e, 'test2@test.com')

    def test_show_this_user_details_by_id(self):
        if not self.client.login(username='test2', password='password'):
            self.fail('User could not login.')
        response = self.client.get(reverse('user:user_id', kwargs={'id': 3}))
        self.assertEquals(response.status_code, 200)
        f = response.data['user']['first_name']
        l = response.data['user']['last_name']
        e = response.data['user']['email']
        lang1 = response.data['first_language'].upper()
        lang2 = response.data['second_language'].upper()
        lang3 = response.data['third_language'].upper()
        self.assertEqual(lang1, 'ENGLISH')
        self.assertEqual(lang2, 'ISIZULU')
        self.assertEqual(lang3, 'SOUTH_AFRICAN_SIGN_LANGUAGE')
        self.assertEqual(f, 'first2')
        self.assertEqual(l, 'last2')
        self.assertEqual(e, 'test2@test.com')

    def test_show_this_user_details_by_id_not_exist(self):
        if not self.client.login(username='admin', password='wellthen'):
            self.fail('User could not login.')
        response = self.client.get(reverse('user:user_id', kwargs={'id': 99}))
        self.assertEquals(response.status_code, 400)

    def test_show_get_user_details_not_admin(self):
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.get(reverse('user:user_id', kwargs={'id': 3}))
        self.assertEquals(response.status_code, 403)

    def test_show_get_user_details_admin(self):
        if not self.client.login(username='admin', password='wellthen'):
            self.fail('User could not login.')
        response = self.client.get(reverse('user:user_id', kwargs={'id': 3}))
        self.assertEquals(response.status_code, 200)

    def test_change_this_user_first_language(self):
        data = {
            # "first_name": "first3",
            # "last_name": "last3",
            # "email": "test3@test.com",
            "first_language": "NSO-ZA",
            # "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        lang1 = response.data['first_language'].upper()
        self.assertEqual(lang1, 'SESOTHO_SA_LEBOA')

    def test_change_this_user_first_language_does_not_exists(self):
        data = {
            # "first_name": "first3",
            # "last_name": "last3",
            # "email": "test3@test.com",
            "first_language": "NSO-ZW",
            # "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 400)

    def test_change_this_user_second_language(self):
        data = {
            # "first_name": "first3",
            # "last_name": "last3",
            # "email": "test3@test.com",
            # "first_language": "ENG-ZA",
            "second_language": "SSO-ZA",
            # "third_language": "XHO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        lang2 = response.data['second_language'].upper()
        self.assertEqual(lang2, 'SESOTHO')

    def test_change_this_user_third_language(self):
        data = {
            # "first_name": "first3",
            # "last_name": "last3",
            # "email": "test3@test.com",
            # "first_language": "ENG-ZA",
            # "second_language": "SHO-ZW",
            "third_language": "AFR-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        lang3 = response.data['third_language'].upper()
        self.assertEqual(lang3, 'AFRIKAANS')

    def test_change_this_user_all_languages(self):
        data = {
            # "first_name": "first3",
            # "last_name": "last3",
            # "email": "test3@test.com",
            "first_language": "AFR-ZA",
            "second_language": "ZUL-ZA",
            "third_language": "SSO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        lang1 = response.data['first_language'].upper()
        lang2 = response.data['second_language'].upper()
        lang3 = response.data['third_language'].upper()
        self.assertEqual(lang1, 'AFRIKAANS')
        self.assertEqual(lang2, 'ISIZULU')
        self.assertEqual(lang3, 'SESOTHO')

    def test_change_this_first_name(self):
        data = {
            "first_name": "f1",
            # "last_name": "last3",
            # "email": "test3@test.com",
            # "first_language": "ENG-ZA",
            # "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        f = response.data['user']['first_name']
        self.assertEqual(f, 'f1')

    def test_change_this_last_name(self):
        data = {
            # "first_name": "first3",
            "last_name": "l1",
            # "email": "test3@test.com",
            # "first_language": "ENG-ZA",
            # "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        l = response.data['user']['last_name']
        self.assertEqual(l, 'l1')

    def test_change_this_email(self):
        data = {
            # "first_name": "first3",
            # "last_name": "last3",
            "email": "email@test.com",
            # "first_language": "ENG-ZA",
            # "second_language": "SHO-ZW",
            # "third_language": "XHO-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        e = response.data['user']['email']
        self.assertEqual(e, 'email@test.com')

    def test_change_all_details(self):
        data = {
            "first_name": "changed1",
            "last_name": "changed2",
            "email": "changed3@test.com",
            "first_language": "SSL-ZA",
            "second_language": "NDE-ZA",
            "third_language": "ZUL-ZA",
        }
        if not self.client.login(username='test1', password='password'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 200)
        f = response.data['user']['first_name']
        l = response.data['user']['last_name']
        e = response.data['user']['email']
        lang1 = response.data['first_language'].upper()
        lang2 = response.data['second_language'].upper()
        lang3 = response.data['third_language'].upper()
        self.assertEqual(lang1, 'SOUTH_AFRICAN_SIGN_LANGUAGE')
        self.assertEqual(lang2, 'ISINDEBELE')
        self.assertEqual(lang3, 'ISIZULU')
        self.assertEqual(f, 'changed1')
        self.assertEqual(l, 'changed2')
        self.assertEqual(e, 'changed3@test.com')

    def test_admin_change_details(self):
        """
        Admin must not be able to change is/her details
        :return:
        """
        data = {
            "first_name": "changed1",
            "last_name": "changed",
            "email": "changed3@test.com",
            "first_language": "SSL-ZA",
            "second_language": "NDE-ZA",
            "third_language": "ZUL-ZA",
        }

        if not self.client.login(username='admin', password='wellthen'):
            self.fail('User could not login.')
        response = self.client.post(reverse('user:user'), data)
        self.assertEquals(response.status_code, 400)


class UserAuth(TestCase):
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
    ]

    def test_get_authentication_token(self):
        url = reverse('user:auth_token')
        data = {
            'username': 'test1',
            'password': 'password'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.__contains__('token'))
