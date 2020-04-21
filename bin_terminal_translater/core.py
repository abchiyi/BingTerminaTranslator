import pyperclip
import requests
import json
import os


def translator(setting, text, language_code) -> str:

    dtb = setting.data_table.copy()
    dtb['data']['to'] = language_code
    dtb['data']['text'] = text

    try:
        response = requests.post(**dtb)
        return response.json()[0]['translations'][0]['text']
    except KeyError:
        raise Exception('SERVER ERROR')
