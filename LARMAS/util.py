import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from user.models import Language, UserProfile


def create_one_time_profile(post, temp_user=User()):
    """
    Function to create a new one-time contributing user
    :param temp_user: user object to populat
    :param post: dictionary (usually request.POST) with new user details
    :return: a new one-time user
    """
    # get first language details.
    try:
        first_lang_code = post.get('first_language', 'x')
        first_lang = Language.objects.get(code=first_lang_code)
    except ObjectDoesNotExist as e:
        raise e

    # try get second language
    try:
        sec_lang_code = post.get('second_language', 'x')
        second_lang = Language.objects.get(code=sec_lang_code)
    except ObjectDoesNotExist:
        second_lang = None

    # try get third language
    try:
        third_lang_code = post.get('third_language', 'x')
        third_lang = Language.objects.get(code=third_lang_code)
    except ObjectDoesNotExist:
        third_lang = None

    # try get the age
    try:
        age = int(post.get('age', '?'))
    except ValueError:
        age = 0

    # save user to generate a new pk
    temp_user.username = 'temp_user_' \
                         + str(uuid.uuid4()) + '_' + str(uuid.uuid4())
    temp_user.is_active = False
    temp_user.set_password(str(uuid.uuid4()))
    temp_user.save()

    # create user profile
    temp_profile = UserProfile(
        user=temp_user,
        age=age,
        first_language=first_lang,
        second_language=second_lang,
        third_language=third_lang
    )
    temp_profile.save()
    # create unique username

    return temp_user


def upload_is_valid(file, source):
    """
    Function to check if the uploaded WAV file is valid
    :param file: uploaded WAV file
    :return: True if file is valid
    """
    if source == 'UPLOAD':
        if not file.name.endswith('wav'):
            raise ValidationError("Wrong file format")
    else:
        # perform more strict file validation
        pass

    return True
