import xml.etree.ElementTree as ElementTree

from django.contrib.auth.models import User

from prompts.models import Prompt
from translations.models import PromptTranslation
from user.models import Language

e = ElementTree.parse('extra/en_GB-sn.xml')
e = e.getroot()
for tuv in e[1]:
    af = Prompt(text=tuv[0][0].text, language=Language.objects.get(code='ENG-ZA'))
    af.save()
    Prompt(text=tuv[1][0].text, language=Language.objects.get(code='SHO-ZW')).save()
    PromptTranslation(language=Language.objects.get(code='SHO-ZW'), text=tuv[1][0].text,original_prompt=af,user=User.objects.get(pk=1),verified=True).save()
