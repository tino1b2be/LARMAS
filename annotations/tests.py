import os
import shutil
import uuid

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from LARMAS.settings import BASE_DIR


class TestUploadRecordings(APITestCase):
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
        'distributed_prompts.json',
    ]

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_recording(self):

        if self.client.login(username='test1', password='password'):
            annotation = str(uuid.uuid4())
            url = reverse('annotations:upload')
            file = open('test_data/files/tom.wav', 'rb')
            data = {
                'file': file,
                'prompt': 1,
                'annotation': annotation,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['annotation'], annotation)
            self.assertEqual(response.data['user'], 'test1')
            self.assertEqual(response.data['prompt'], 1)
            self.assertTrue(response.data.__contains__('file_url'))
        else:
            self.fail('User could not login.')

        # remove test files
        if os.path.isdir('test_media'):
            shutil.rmtree('test_media')

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_recording_no_file(self):
        annotation = str(uuid.uuid4())
        url = reverse('annotations:upload')
        # file = open('test_data/files/tom.wav', 'rb')
        if self.client.login(username='test1', password='password'):
            data = {
                # 'file': file,
                'prompt': 1,
                'annotation': annotation,
            }
            response = self.client.post(url, data)
            # file.close()
            self.assertEqual(response.status_code, 400)

        else:
            self.fail('User could not login.')

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_recording_no_prompt(self):
        annotation = str(uuid.uuid4())
        url = reverse('annotations:upload')
        file = open('test_data/files/tom.wav', 'rb')
        if self.client.login(username='test1', password='password'):
            data = {
                'file': file,
                # 'prompt': 1,
                'annotation': annotation,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 400)

        else:
            self.fail('User could not login.')

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_recording_no_annotation(self):
        url = reverse('annotations:upload')
        file = open('test_data/files/tom.wav', 'rb')
        if self.client.login(username='test1', password='password'):
            data = {
                'file': file,
                'prompt': 1,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 400)

        else:
            self.fail('User could not login.')

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_recording_short_filename(self):
        annotation = str(uuid.uuid4())
        url = reverse('annotations:upload')
        file = open('test_data/files/wav', 'rb')

        if self.client.login(username='test1', password='password'):
            data = {
                'file': file,
                'prompt': 1,
                'annotation': annotation,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 400)

        else:
            self.fail('User could not login.')

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_unauthorized_prompt(self):
        """
        test to check if user uploads a prompt they were not given
        :return:
        """
        annotation = str(uuid.uuid4())
        url = reverse('annotations:upload')
        file = open('test_data/files/tom.wav', 'rb')

        if self.client.login(username='test1', password='password'):
            data = {
                'file': file,
                'prompt': 15,
                'annotation': annotation,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 400)

        else:
            self.fail('User could not login.')

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_prompt_does_not_exist(self):
        """
        test to check if user uploads a prompt they were not given
        :return:
        """
        annotation = str(uuid.uuid4())
        url = reverse('annotations:upload')
        file = open('test_data/files/tom.wav', 'rb')

        if self.client.login(username='test1', password='password'):
            data = {
                'file': file,
                'prompt': 999,
                'annotation': annotation,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 400)

        else:
            self.fail('User could not login.')


class TestListRecordings(APITestCase):
    fixtures = [
        'prompts_test.json',
        'language_test.json',
        'user_test.json',
        'user_profile_test.json',
        'distributed_prompts.json',
    ]

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_get_all_recordings(self):
        if self.client.login(username='admin', password='wellthen'):
            url = reverse('annotations:list')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
        else:
            self.fail("User could not login.")

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_get_one_recording(self):

        if self.client.login(username='test1', password='password'):
            annotation = str(uuid.uuid4())
            url = reverse('annotations:upload')
            file = open('test_data/files/tom.wav', 'rb')
            data = {
                'file': file,
                'prompt': 1,
                'annotation': annotation,
            }
            responsex = self.client.post(url, data)
            file.close()
            self.client.logout()
            if responsex.status_code == 201 and \
                    self.client.login(username='admin', password='wellthen'):
                url = reverse('annotations:recording', kwargs={'pk': 1})
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
            else:
                self.fail('Could not upload recording.')
        else:
            self.fail("User could not login.")

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_get_recordings_not_admin(self):

        if self.client.login(username='test1', password='password'):
            url1 = reverse('annotations:list')
            url2 = reverse('annotations:recording', kwargs={'pk': 1})
            response1 = self.client.get(url1)
            response2 = self.client.get(url2)
            self.assertEqual(response1.status_code, 403)
            self.assertEqual(response2.status_code, 403)
        else:
            self.fail('User could not login.')
