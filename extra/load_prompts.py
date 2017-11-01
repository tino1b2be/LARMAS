import xml.etree.ElementTree as ElementTree

from django.contrib.auth.models import User
from django.db import transaction

from prompts.models import Prompt
from translations.models import PromptTranslation
from user.models import Language

e = ElementTree.parse('extra/en_GB-sn.xml')
e = e.getroot()
i = 0
with transaction.atomic():
    for tuv in e[1]:
        i += 1
        if i < 61:
            continue
        af = Prompt(text=tuv[0][0].text, language=Language.objects.get(code='ENG-ZA'))
        af.save()
        Prompt(text=tuv[1][0].text, language=Language.objects.get(code='SHO-ZW')).save()
        PromptTranslation(language=Language.objects.get(code='SHO-ZW'), text=tuv[1][0].text,original_prompt=af,user=User.objects.get(pk=1),verified=True).save()
        print('ENG-SHO %s' % i)

e = ElementTree.parse('extra/af-en_GB.xml')
e = e.getroot()
i = 0
with transaction.atomic():
    for tuv in e[1]:

        i += 1
        af = Prompt(text=tuv[0][0].text, language=Language.objects.get(code='AFR-ZA'))
        af.save()
        Prompt(text=tuv[1][0].text, language=Language.objects.get(code='ENG-ZA')).save()
        PromptTranslation(language=Language.objects.get(code='ENG-ZA'), text=tuv[1][0].text,original_prompt=af,user=User.objects.get(pk=1),verified=True).save()
        print('AFR-ENG %d' % i)
