
import uuid
import requests
import json

# from prompts.models import Prompt

url_reg = 'http://0.0.0.0:8000/v1/user/register/'
url_token = 'http://0.0.0.0:8000/v1/user/api-token-auth/'
url_prompts = 'http://0.0.0.0:8000/v1/prompts/retrieve/'
url_upload = 'http://0.0.0.0:8000/v1/annotations/upload/'
num_users = 2000
total = num_users*50
count = 50

# loop 2000 times for 2000 users
for i in range(1000,num_users):
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

    print('User - %s created' % data['username'])

    # user successfully created
    data = {
        "username": "experiment_dist_%s" % i,
        "password": "password",
    }
    # get auth token
    response = requests.post(url_token, data=data)
    if not response.status_code // 200 == 1:
        raise Exception("couldn't get token.")

    print('Token received.')
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

    print('Prompts received.')
    prompts = json.loads(response.text)

    count2 = 0
    max = len(prompts)
    for prompt in prompts:
        # upload an annotation for each prompt.
        file = open('tom.wav', 'rb')
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
        if not response.status_code // 200 == 1:
            raise Exception('could not upload.')

        count += 1
        count2 += 1
        print('Prompt %d of %d uploaded for user (%d/%d total).' % (count2, max, count, total))

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