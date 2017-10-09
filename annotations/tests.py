import os
import shutil

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from LRMS_Thesis.settings import BASE_DIR


class TestAnnotationsViews(TestCase):
    fixtures = [
        'annotations.json',
        'frequency.json',
        'language.json',
        'user.json',
        'user_profile.json',
    ]

    def test_get_annotation_by_id(self):
        if self.client.login(username='test1', password='password'):
            response1 = self.client.get(
                reverse('annotations:annotation', kwargs={'pk': 1})
            )
            response2 = self.client.get(
                reverse('annotations:annotation', kwargs={'pk': 3})
            )
            self.assertEquals(response1.status_code, 200)
            self.assertEquals(response2.status_code, 200)
        else:
            return self.fail('User could not login.')

    def test_get_annotation_by_id_not_exist(self):
        if self.client.login(username='test1', password='password'):
            response1 = self.client.get(
                reverse('annotations:annotation', kwargs={'pk': 999})
            )
            response2 = self.client.get(
                reverse('annotations:annotation', kwargs={'pk': 888})
            )
            self.assertEquals(response1.status_code, 404)
            self.assertEquals(response2.status_code, 404)
        else:
            return self.fail('User could not login.')

    def test_list_all_annotations(self):
        if self.client.login(username='test1', password='password'):
            response = self.client.get(reverse('annotations:annotations'))
            self.assertEquals(response.status_code, 200)
        else:
            return self.fail('User could not login.')

    def test_create_annotation_missing_language(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'This is a test',
            }
            r = self.client.post(reverse('annotations:annotations'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_create_annotation_missing_text(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'language': 'ENG-ZA',
            }
            r = self.client.post(reverse('annotations:annotations'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_unsupported_language(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'This is a test',
                'language': 'ENG-ZW'
            }
            r = self.client.post(reverse('annotations:annotations'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_annotation_too_short(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'T',
                'language': 'ENG-ZA'
            }
            r = self.client.post(reverse('annotations:annotations'), data)
            self.assertEquals(r.status_code, 400)
        else:
            self.fail('User could not log in.')

    def test_create_annotation(self):
        if self.client.login(username='admin', password='wellthen'):
            data = {
                'text': 'This is a test.',
                'language': 'ENG-ZA',
            }
            r = self.client.post(reverse('annotations:annotations'), data)
            self.assertEquals(r.status_code, 201)
        else:
            self.fail('User could not log in.')


class TestRecordingsViews(APITestCase):
    fixtures = [
        'annotations.json',
        'frequency.json',
        'language.json',
        'user.json',
        'user_profile.json',
    ]

    @override_settings(MEDIA_URL='/test_media/',
                       MEDIA_ROOT=os.path.join(BASE_DIR, 'test_media'))
    def test_upload_recording(self):

        url = reverse('annotations:upload_recording')
        file = open('extra/tom.wav', 'rb')
        if self.client.login(username='test1', password='password'):
            data = {
                'file': file,
                'annotation': 1,
            }
            response = self.client.post(url, data)
            file.close()
            self.assertEqual(response.status_code, 201)
        else:
            self.fail('User could not login.')

        # remove test files
        shutil.rmtree('test_media')
