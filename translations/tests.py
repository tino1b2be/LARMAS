from rest_framework.test import APITestCase


class TestTranslationUpload(APITestCase):

    def test_upload_translation_correct(self):
        # todo
        self.fail()

    def test_upload_translation_no_language(self):
        # todo
        self.fail()

    def test_upload_translation_no_original_prompt(self):
        # todo
        self.fail()

    def test_upload_translation_unknown_original_prompt(self):
        # todo
        self.fail()

    def test_upload_translation_unsupported_language(self):
        # todo
        self.fail()

    def test_upload_translation_no_text_field(self):
        # todo
        self.fail()


class TestTranslationDetails(APITestCase):

    def test_show_translations_all_not_allowed(self):
        self.fail()

    def test_show_translations_all(self):
        self.fail()

    def test_show_translation_by_id(self):
        self.fail()

    def test_show_translation_wrong_id(self):
        self.fail()

    def test_show_translations_parallel(self):
        self.fail()

    def test_show_translations_parallel_unsupported_first(self):
        self.fail()

    def test_show_translations_parallel_unsupported_second(self):
        self.fail()
