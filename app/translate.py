import json
import requests
from flask_babel import _
from app import webapp


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in webapp.config or not webapp.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    headers = {
        'Ocp-Apim-Subscription-Key': webapp.config['MS_TRANSLATOR_KEY'],
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': str(len(text))
        }
    url_params = {
        'api-version': '3.0',
        'to': dest_language,
        'from': source_language
    }
    payload = [{
        'Text': text
    }]
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com/translate',
        headers=headers,
        params=url_params,
        data=json.dumps(payload),
    )
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))[0]['translations'][0]["text"]
