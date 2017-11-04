
import uuid
import requests
import json

from prompts.models import Prompt

url_reg = 'http://0.0.0.0:8000/v1/user/register/'
url_token = 'http://0.0.0.0:8000/v1/user/api-token-auth/'
url_prompts = 'http://0.0.0.0:8000/v1/prompts/retrieve/'
url_upload = 'http://0.0.0.0:8000/v1/annotations/upload/'

# loop 200 times for 200 users
for i in range(2000):
    # create user
    data = {
        "username": "experiment_dist_%s" % i,
        "password": "password",
        "first_language": "SHO-ZW",
    }
    response = requests.post(
        url_reg,
        data=data,
        # headers={'content-type': 'application/json'}
    )

    if not response.status_code // 200 == 1:
        raise Exception("couldn't create user.")

    # user successfully created
    data = {
        "username": "experiment_dist_%s" % i,
        "password": "password",
    }
    # get auth token
    response = requests.post(url_token, data=data)
    if not response.status_code // 200 == 1:
        raise Exception("couldn't get token.")

    body = json.loads(response.text)
    token = body['token']

    # token obtained. Now retrieve prompts for this user.
    headers = {
        # 'content-type': 'application/json',
        'Authorization': 'Token %s' % token,
    }
    response = requests.get(url_prompts, headers=headers)
    if not response.status_code // 200 == 1:
        raise Exception("couldn't get prompts.")

    prompts = json.loads(response.text)

    for prompt in prompts:
        # upload an annotation for each prompt.
        file = open('test_data/files/tom.wav', 'rb')
        data = {
            'prompt': prompt['id'],
            'annotation': uuid.uuid4(),
        }
        response = requests.post(
            url_upload,
            data=data,
            files={'file': file},
            headers=headers,
        )
        s = response.status_code

    # done uploading annotations

# load data to CVS files

queryset = Prompt.objects.filter(language__code='SHO-ZW')
results = []
f = open('results.txt', 'w')
f.write('Prompt ID, Number of recordings\n')
for rec in queryset:
    record = "%s, %s\n" % (str(rec.id), str(rec.number_of_recordings))
    f.write(record)

# done with experiment!