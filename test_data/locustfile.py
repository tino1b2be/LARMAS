import random
import uuid
import json

from locust import HttpLocust, TaskSet, task

num_prompts = 28252
headers_default = {'Content-type': 'application/json'}

token_admin = {
    'Content-type': 'application/json',
    "Authorization": "Token 7f613e51d4d0227492b7c85d80913a3eeb6aef4f"
}

url_upload_ann = "/v1/annotations/upload/"
url_upload_tran = '/v1/prompt_translations/upload/'
url_profile = '/v1/user/'
url_add_prompt = '/v1/prompts/'
url_all_ann = '/v1/annotations/'

wav_file = open('files/tom.wav', 'rb')
wav_file.close()

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

        data = {
            'prompt': random.randint(1, 28252),
            'annotation': str(uuid.uuid4()),
            'first_language': random.choice(languages),
            "age": 23,

        }
        self.client.post(url_upload_ann, data=json.dumps(data))

    @task(30)
    def upload_translation(self):
        data = {
            'text': str(uuid.uuid4()),
            'original_prompt': random.randint(1, 28252),
            'language': random.choice(languages),
        }

        self.client.post(url_upload_tran, data=json.dumps(data))

    @task(15)
    def add_prompt(self):
        data = {
            'text': str(uuid.uuid4()),
            'language': random.choice(languages),
        }
        self.client.post(url_add_prompt, data=json.dumps(data))

    @task(10)
    def get_parallel(self):
        url = '/v1/prompt_translations/parallel/ENG-ZA/SHO-ZW/'
        self.client.get(url)

    @task(10)
    def get_all_annotations(self):
        self.client.get(url_all_ann)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 500