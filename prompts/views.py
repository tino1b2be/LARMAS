import random

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, \
    HTTP_406_NOT_ACCEPTABLE, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from constance import config

from LARMAS.settings import DEBUG
from user.models import UserProfile, Language
from prompts.models import Prompt, DistributedPrompt
from prompts.serializers import PromptSerializer


class PromptsView(ListAPIView):
    """
    Response class to return all prompts or create a new prompt
    """

    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        create new prompt
        :return: created prompt or error messages.
        """

        # check if fields exist

        if not request.user.is_staff:
            data = {
                'detail': 'Only admin users are allowed to add new prompts.',
            }
            return Response(data, status=HTTP_401_UNAUTHORIZED)

        if not request.data.__contains__('language'):
            data = {
                'message': 'language field is required',
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        if not request.data.__contains__('text'):
            data = {
                'message': 'text field is required',
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        # get the language code and create prompt
        try:
            language = Language.objects.get(code=request.data['language'])
            text = request.data['text']
            if len(text) < 2:
                data = {
                    'message': 'Prompt is too short',
                }
                return Response(data, status=HTTP_400_BAD_REQUEST)
            prompt = Prompt(text=text, language=language)
            prompt.save()
            serializer = PromptSerializer(prompt)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except ObjectDoesNotExist:
            data = {
                'message': 'That language is not supported.',
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = str(e) if DEBUG else 'An error has occurred'
            data = {'message': message}
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class PromptDetail(RetrieveAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = (IsAdminUser,)


class PromptDistribution(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Get request to distribute prompts
        :param request:
        :return:
        """
        data = {'detail': ''}
        try:
            user = request.user
            if not user.is_authenticated:
                # just respond with a random prompt
                try:
                    language = request.query_params.get('language', 'x')
                    prompts = Prompt.objects.filter(language__code=language)
                    if prompts.count() == 0:
                        raise ObjectDoesNotExist()
                    prompt = random.choice(prompts)
                    s = PromptSerializer(prompt)
                    return Response(s.data, status=HTTP_200_OK)
                except ObjectDoesNotExist:
                    data['detail'] = 'No prompts found. Please ' \
                                     'verify the language GET parameter.'
                    return Response(data, HTTP_400_BAD_REQUEST)

            profile = UserProfile.objects.get(user=user)
            lang_code = request.GET.get('language', 'X')

            if lang_code == 'X':
                language = profile.first_language
            else:
                try:
                    language = Language.objects.get(code=lang_code)
                    if not (
                            profile.first_language == language or
                            profile.second_language == language or
                            profile.third_language == language):
                        data['detail'] = "language in user's profile"
                        return Response(data, status=HTTP_400_BAD_REQUEST)
                except ObjectDoesNotExist:
                    data['detail'] = 'language does not exist'
                    return Response(data, status=HTTP_400_BAD_REQUEST)

            # send all unrejected/unrecorded prompts
            dist_prompts = DistributedPrompt \
                .objects \
                .filter(user=user,
                        rejected=False,
                        recorded=False,
                        prompt__language=language
                        )

            id_list = []
            for dist_prompt in dist_prompts:
                id_list.append(dist_prompt.prompt.id)

            ps = Prompt.objects.filter(id__in=id_list)
            prompts = []
            for p in ps:
                prompts.append(p)

            # if there are not enough distributed prompts, add more.

            queryset = Prompt.objects.all()
            if not config.RANDOM_DISTRIBUTION:
                queryset.order_by('number_of_recordings')
            i = 0
            size = len(queryset)
            cache = []  # cache tp keep track of checked prompts

            # add prompts until
            # 1) user has enough prompts
            # 2) user rejected all prompts
            while len(prompts) < config.PROMPTS_PER_USER \
                    and (i < size) \
                    and len(cache) > len(prompts) - 1:

                # get a random prompt if random parameter is set
                if config.RANDOM_DISTRIBUTION:
                    prompt = random.choice(queryset)
                    if prompts.__contains__(prompt):
                        continue
                    # add to cache
                    cache.append(prompt)
                else:
                    # get prompt with least number of recordings
                    prompt = queryset[i]

                dist = DistributedPrompt \
                    .objects \
                    .filter(user=user, prompt=prompt)
                if dist.count() == 0:
                    # this prompt has not been distributed.
                    if prompt.language == language:
                        prompts.append(prompt)
                        # add this prompt to the distributed prompts database
                        DistributedPrompt(user=user, prompt=prompt).save()
                        # next prompt
                        i += 1
                        # else:
                        #     # wrong language
                        #     continue

            # serialize all prompts and respond to request.
            s = PromptSerializer(prompts, many=True)
            return Response(s.data, status=HTTP_200_OK)

        except Exception as e:
            data['detail'] = str(e) if DEBUG else 'Something went wrong.'
            return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)


class PromptRejection(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request, pk):
        data = {'detail': ''}
        try:
            user = request.user
            try:
                prompt = Prompt.objects.get(id=pk)
                dp = DistributedPrompt.objects.get(user=user, prompt=prompt)
                dp.rejected = True
                dp.save()
                data['detail'] = 'Prompt ID = %s has been rejected' % pk
                return Response(data, HTTP_200_OK)

            except ObjectDoesNotExist:
                data['detail'] = 'This annotation was not give to you'
                return Response(data, status=HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            data['detail'] = str(e) if DEBUG else 'Something went wrong.'
            pass
