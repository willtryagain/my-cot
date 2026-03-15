import json
import urllib.request
import time 
from schema import Card

def card_stream(source: str, path: str | None = None):
    if source == "file":
        if not path:
            raise ValueError("`path` is required when using file")
        print(f"streaming from file path: {path}")
        
        return iter_question_file(path=path)
    if source == "anki":
        print("streaming from anki connect!")
        return iter_anki_connect()
    raise ValueError(f"`source` {source} not found")


def iter_question_file(path='/home/a/Downloads/python.txt'):
    with open(path) as f:
        for line in f.readlines():
            if not len(line) or '#' == line[0] or len(line.split('\t')) != 6:
                continue
            card_id, _, _, question, solution, _ = line.split('\t')
            card_id = path + card_id
            card = Card(id=card_id, question=question, solution=solution) 
            yield card

def iter_anki_connect():
    def request(action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def invoke(action, **params):
        requestJson = json.dumps(request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']
    previous_card_id = -1
    while True:
        try:
            result = invoke('guiCurrentCard')
        except Exception as e:
            if e == 'Gui review is not currently active.':
                print(e)
                time.sleep(10)
                continue
            raise e
        if previous_card_id == result['cardId']:
            time.sleep(1)
            continue
        card = Card(
            id=str(result['cardId']), 
            question=result['fields']['Front']['value'], 
            solution=result['fields']['Back']['value']
        ) 
        yield card
        previous_card_id = card.id

