from django.urls import reverse
from rest_framework.test import APITestCase

from LARMAS.settings import PROMPTS_PER_USER


class TestPromptViews(APITestCase):
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
        'distributed_prompts.json',
    ]

    def test_get_prompt_by_id(self):
        if self.client.login(username='admin', password='wellthen'):
            response1 = self.client.get(
                reverse('prompts:prompt', kwargs={'pk': 1})
            )
            response2 = self.client.get(
                reverse('prompts:prompt', kwargs={'pk': 3})
            )
            self.assertEquals(response1.status_code, 200)
            self.assertEquals(response2.status_code, 200)
        else:
            return self.fail('User could not login.')

    def test_get_prompt_by_id_not_exist(self):
        if self.client.login(username='admin', password='wellthen'):
            response1 = self.client.get(
                reverse('prompts:prompt', kwargs={'pk': 999})
            )
            response2 = self.client.get(
                reverse('prompts:prompt', kwargs={'pk': 888})
            )
            self.assertEquals(response1.status_code, 404)
            self.assertEquals(response2.status_code, 404)
        else:
            return self.fail('User could not login.')

    def test_list_all_prompts(self):
        if self.client.login(username='admin', password='wellthen'):
            response = self.client.get(reverse('prompts:prompts'))
            self.assertEquals(response.status_code, 200)
        else:
            return self.fail('User could not login.')

    def test_create_prompt_missing_language(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'This is a test',
            }
            r = self.client.post(reverse('prompts:prompts'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_create_prompt_missing_text(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'language': 'ENG-ZA',
            }
            r = self.client.post(reverse('prompts:prompts'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_create_prompt_unsupported_language(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'This is a test',
                'language': 'ENG-ZW'
            }
            r = self.client.post(reverse('prompts:prompts'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_create_prompt_too_short(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'T',
                'language': 'ENG-ZA'
            }
            r = self.client.post(reverse('prompts:prompts'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_create_prompt(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'This is a test.',
                'language': 'ENG-ZA',
            }
            r = self.client.post(reverse('prompts:prompts'), data)
            self.assertEquals(r.status_code, 201)
        else:
            self.fail('User could not log in.')


class TestPromptDistribution(APITestCase):
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
    ]

    def test_get_prompts_first_language(self):

        if self.client.login(username='test2', password='password'):
            # get prompts
            url = reverse('prompts:retrieve')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), PROMPTS_PER_USER)

            # test the languages
            for prompt in response.data:
                self.assertEqual(prompt['language'].upper(), 'ENGLISH')

        else:
            self.fail('User could not log in.')

    def test_get_prompts_second_language(self):

        if self.client.login(username='test1', password='password'):
            url = "%s?language=SHO-ZW" \
                  % reverse('prompts:retrieve')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), PROMPTS_PER_USER)

            # test the languages
            for prompt in response.data:
                self.assertEqual(prompt['language'].upper(), 'CHISHONA')
        else:
            self.fail('User could not log in.')

    def test_get_prompts_language_does_not_exist(self):

        if self.client.login(username='test1', password='password'):
            url = "%s?language=SHO-ZA" \
                  % reverse('prompts:retrieve')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_get_prompts_language_not_in_users_profile(self):

        if self.client.login(username='test1', password='password'):
            url = "%s?language=NSO-ZA" \
                  % reverse('prompts:retrieve')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_get_prompts_third_language(self):
        # todo add Xhosa data for third language
        pass

    def test_get_prompts_twice_no_rejection(self):

        if self.client.login(username='test2', password='password'):
            # get prompts
            url = reverse('prompts:retrieve')
            response1 = self.client.get(url)

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(len(response1.data), PROMPTS_PER_USER)

            prompts = []
            # save all the prompts temporarily
            for prompt in response1.data:
                prompts.append(prompt['text'])

            # request for prompts again
            response2 = self.client.get(url)

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(len(response1.data), PROMPTS_PER_USER)

            # check if the same prompts were returned
            for prompt in response2.data:
                self.assertTrue(prompt['text'] in prompts)

        else:
            self.fail('User could not log in.')

    def test_get_prompts_after_rejection(self):

        if self.client.login(username='test1', password='password'):
            get_prompts = reverse('prompts:retrieve')
            response1 = self.client.get(get_prompts)

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(len(response1.data), PROMPTS_PER_USER)

            # reject the first and fifth prompts
            p_1 = response1.data[0]['id']
            p_1_text = response1.data[0]['text']
            p_2 = response1.data[4]['id']
            p_2_text = response1.data[4]['text']

            # send request to reject
            url1 = reverse('prompts:reject', kwargs={'pk': p_1})
            url2 = reverse('prompts:reject', kwargs={'pk': p_2})

            response2 = self.client.get(url1)
            response3 = self.client.get(url2)
            response4 = self.client.get(get_prompts)

            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response3.status_code, 200)
            # check if the old prompts are in the new prompts list
            prompts = []
            for prompt in response4.data:
                prompts.append(prompt['text'])

            self.assertFalse(p_1_text in prompts)
            self.assertFalse(p_2_text in prompts)

    def test_reject_wrong_prompt(self):

        if self.client.login(username='test2', password='password'):
            get_prompts = reverse('prompts:retrieve')
            response1 = self.client.get(get_prompts)

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(len(response1.data), PROMPTS_PER_USER)

            url = reverse('prompts:reject', kwargs={'pk': 999})
            response2 = self.client.get(url)

            self.assertEqual(response2.status_code, 406)
