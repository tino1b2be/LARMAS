from django.test import TestCase
from django.urls import reverse


class TestAnnotationsViews(TestCase):

    fixtures = [
        'annotations.json',
        'frequency.json',
        'language.json',
        'user.json',
        'user_profile.json',
    ]

    def test_get_annotation_by_id(self):
        response1 = self.client.get(
            reverse('annotations:annotation', kwargs={'pk': 1})
        )
        response2 = self.client.get(
            reverse('annotations:annotation', kwargs={'pk': 3})
        )
        self.assertEquals(response1.status_code, 200)
        self.assertEquals(response2.status_code, 200)

    def test_get_annotation_by_id_not_exist(self):
        response1 = self.client.get(
            reverse('annotations:annotation', kwargs={'pk': 999})
        )
        response2 = self.client.get(
            reverse('annotations:annotation', kwargs={'pk': 888})
        )
        self.assertEquals(response1.status_code, 404)
        self.assertEquals(response2.status_code, 404)

    def test_list_all_annotations(self):
        response = self.client.get(reverse('annotations:annotations'))
        self.assertEquals(response.status_code, 200)

    def test_create_annotation_missing_language(self):
        data = {
            'text': 'This is a test',
        }
        response = self.client.post(reverse('annotations:annotations'), data)
        self.assertEquals(response.status_code, 400)

    def test_create_annotation_missing_text(self):
        data = {
            'language': 'ENG-ZA',
        }
        response = self.client.post(reverse('annotations:annotations'), data)
        self.assertEquals(response.status_code, 400)

    def test_unsupported_language(self):
        data = {
            'text': 'This is a test',
            'language': 'ENG-ZW'
        }
        response = self.client.post(reverse('annotations:annotations'), data)
        self.assertEquals(response.status_code, 400)

    def test_annotation_too_short(self):
        data = {
            'text': 'T',
            'language': 'ENG-ZA'
        }
        response = self.client.post(reverse('annotations:annotations'), data)
        self.assertEquals(response.status_code, 400)

    def test_create_annotation(self):
        data = {
            'text': 'This is a test.',
            'language': 'ENG-ZA',
        }
        response = self.client.post(reverse('annotations:annotations'), data)
        self.assertEquals(response.status_code, 201)
