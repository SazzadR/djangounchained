import json
from django.db import models
from django.core import serializers
from django.forms.models import model_to_dict


def debug(input_object, title_text=None):
    terminal_yellow_bg = '\33[43m'
    terminal_blue_bg = '\33[44m'
    terminal_red_bg = '\33[41m'
    terminal_end = '\033[0m'

    if title_text is not None:
        title = '======================== Debugging {} ========================'.format(title_text)
    else:
        title = '======================== Debugging ========================'

    print(terminal_yellow_bg + title + terminal_end + '\n')

    if isinstance(input_object, models.Model):
        print(terminal_blue_bg + json.dumps(model_to_dict(input_object)) + terminal_end)
    elif isinstance(input_object, models.query.QuerySet):
        print(terminal_blue_bg + serializers.serialize('json', input_object) + terminal_end)
    else:
        print(terminal_red_bg + 'Debugger doesn\'t support this format...' + terminal_end)

    print('\n' + terminal_yellow_bg + '========================= End =========================' + terminal_end + '\n')
