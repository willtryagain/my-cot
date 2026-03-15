import sys 
from datetime import datetime
import json
import os 
import signal 
import random
import argparse

import json
import urllib.request

instruction = """
First describe what aspects of the question are you answering,
then describe in full detail. 

"""

def handler(signum, frame):
    print("close after answering! by entering q")
signal.signal(signal.SIGTSTP, handler)

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

def iter_anki_connect():
    while True:
        result = invoke('guiCurrentCard')
        yield result['cardId'], result['fields']['Front']['value'], result['fields']['Back']['value']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path to the tsv Anki file", default='/home/a/Downloads/python.txt')
    parser.add_argument("--out", help="save session as JSONL", default="session.jsonl")
    args = parser.parse_args()
    for card_id, question, solution in iter_anki_connect(): #iter_anki_temp(args.input):
        print(f"\n{instruction} \n\nquestion>{question}")
        thoughts = []
        print("\n<thought> (end with empty line)")
        try: 
            while True:
                cur = input()
                if not cur:
                    break
                thoughts.append(cur)
        except KeyboardInterrupt:
            if len(thoughts) == 0:
                print("skipping..")
                continue
            print("\n</thought>")
        else: 
            print("\n</thought>")
        answer = input("<answer>")        
        print("</answer>")
        print(f"<solution>{solution}</solution>")
        
        score = input("< = > ?")
        session = {
            "card_id": card_id,
            "question": question,
            "solution": solution,
            "answer": answer,
            "score": score,
            "timestamp": datetime.now().isoformat(),
            "thoughts": "\n".join(thoughts)
        }
        with open(args.out, 'a') as f:
            f.write(json.dumps(session) + "\n")
        if input("q to quit: ").strip() == 'q':
            break


if __name__ == "__main__":
    main()
