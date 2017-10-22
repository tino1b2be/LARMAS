from django.urls import reverse
from rest_framework.test import APITestCase


class TestTranslationUpload(APITestCase):
    fixtures = [
        'translations_test.json',
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
        'distributed_prompts.json',
    ]

    def test_upload_translation_correct(self):

        if self.client.login(username='test1', password='password'):
            data = {
                'text': 'Unogara kupi?',
                'original_prompt': 7,
                'language': 'SHO-ZW',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 201)

        else:
            self.fail("Could not login.")

    def test_upload_translation_no_language(self):
        if self.client.login(username='test1', password='password'):
            data = {
                'text': 'Unogara kupi?',
                'original_prompt': 7,
                # 'language': 'SHO-ZW',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 400)

        else:
            self.fail("Could not login.")

    def test_upload_translation_no_original_prompt(self):
        if self.client.login(username='test1', password='password'):
            data = {
                'text': 'Unogara kupi?',
                # 'original_prompt': 7,
                'language': 'SHO-ZW',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 400)

        else:
            self.fail("Could not login.")

    def test_upload_translation_original_prompt_not_given_to_user(self):
        if self.client.login(username='test1', password='password'):
            data = {
                'text': 'Unogara kupi?',
                'original_prompt': 15,
                'language': 'SHO-ZW',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 400)

        else:
            self.fail("Could not login.")

    def test_upload_translation_original_prompt_does_not_exist(self):
        if self.client.login(username='test1', password='password'):
            data = {
                'text': 'Unogara kupi?',
                'original_prompt': 999,
                'language': 'SHO-ZW',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 400)

        else:
            self.fail("Could not login.")

    def test_upload_translation_unsupported_language(self):
        if self.client.login(username='test1', password='password'):
            data = {
                'text': 'Unogara kupi?',
                'original_prompt': 7,
                'language': 'SHO-ZA',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 400)

        else:
            self.fail("Could not login.")

    def test_upload_translation_no_text_field(self):
        if self.client.login(username='test1', password='password'):
            data = {
                # 'text': 'Unogara kupi?',
                'original_prompt': 7,
                'language': 'SHO-ZW',
            }
            url = reverse('translations:upload')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 400)

        else:
            self.fail("Could not login.")


class TestTranslationDetails(APITestCase):
    fixtures = [
        'translations_test.json',
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
        'distributed_prompts.json',
    ]

    def test_show_translations_all(self):

        if self.client.login(username='admin', password='wellthen'):
            url = reverse('translations:translations')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        else:
            self.fail("Could not login.")

    def test_show_translations_all_not_admin(self):

        if self.client.login(username='test1', password='password'):
            url = reverse('translations:translations')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
        else:
            self.fail("Could not login.")

    def test_show_translation_by_id(self):
        if self.client.login(username='admin', password='wellthen'):
            url = reverse('translations:translation', kwargs={'pk': 1})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        else:
            self.fail("Could not login.")

    def test_show_translation_wrong_id(self):
        if self.client.login(username='admin', password='wellthen'):
            url = reverse('translations:translation', kwargs={'pk': 999})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
        else:
            self.fail("Could not login.")

    def test_show_translations_parallel(self):
        if self.client.login(username='admin', password='wellthen'):
            args = {
                'first': 'ENG-ZA',
                'second': 'SHO-ZW'
            }
            url = reverse('translations:parallel', kwargs=args)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        else:
            self.fail("Could not login.")

    def test_show_translations_parallel_unsupported_first(self):
        if self.client.login(username='admin', password='wellthen'):
            args = {
                'first': 'ENG-ZW',
                'second': 'SHO-ZW'
            }
            url = reverse('translations:parallel', kwargs=args)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        else:
            self.fail("Could not login.")

    def test_show_translations_parallel_unsupported_second(self):
        if self.client.login(username='admin', password='wellthen'):
            args = {
                'first': 'ENG-ZA',
                'second': 'SHO-ZA'
            }
            url = reverse('translations:parallel', kwargs=args)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        else:
            self.fail("Could not login.")
