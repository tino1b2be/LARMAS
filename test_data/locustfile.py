import random
import uuid

from locust import HttpLocust, TaskSet, task

num_prompts = 28252
headers_default = {'Content-type': 'application/json'}
token_test1 = {
    'Content-type': 'application/json',
    "Authorization": "Token 189372f71e33d17f40eafd07fbf67ebabad52a5f"
}
token_admin = {
    'Content-type': 'application/json',
    "Authorization": "Token e2d87c5be30862579826090708cbff2b76a1587e"
}

url_upload_ann = "/v1/annotations/upload/"
url_upload_tran = '/v1/prompt_translations/upload/'
url_profile = '/v1/user/'
url_add_prompt = '/v1/prompts/'
url_all_ann = '/v1/annotations/'

wav_file = open('files/tom.wav', 'rb')

languages = [
    'ENG-ZA',
    'AFR-ZA',
    'SHO-ZW',
    'SSO-ZA',
    'SSL-ZA',
    'NSO-ZA',
    'NDE-ZA',
    'ZUL-ZA',
    'XHO-ZA',
    'TSO-ZA',
    'TSW-ZA',
    'SWA-ZA',
    'VEN-ZA',
]


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.headers = token_admin


    @task(35)
    def upload_annotation(self):
        # get prompts

        files = {'file': wav_file}

        data = {
            'prompt': random.randint(1, 28252),
            'annotation': str(uuid.uuid4()),
            'first_language': random.choice(languages),
            "age": 23,

        }
        self.client.post(url_upload_ann, data=data, files=files, headers=headers_default)

    @task(30)
    def upload_translation(self):
        data = {
            'text': str(uuid.uuid4()),
            'original_prompt': random.randint(1, 28252),
            'language': random.choice(languages),
        }

        self.client.post(url_upload_tran, data)

    @task(1)
    def get_profile(self):
        r = self.client.get(url_profile)
        print(r)

    @task(15)
    def add_prompt(self):
        data = {
            'text': str(uuid.uuid4()),
            'language': random.choice(languages),
        }
        self.client.post(url_add_prompt, data=data)

    @task(5)
    def get_parallel(self):
        url = '/v1/prompt_translations/parallel/%s/%s/' % \
              (random.choice(languages), random.choice(languages))
        self.client.get(url)

    @task(5)
    def get_translation(self):
        url = '/v1/prompt_translations/%d/' % random.randint(1, 14113)
        self.client.get(url)

    @task(10)
    def get_all_annotations(self):
        self.client.get(url_all_ann)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000
