import sys 
from datetime import datetime
import json
import os 
import signal 
import argparse

import json
from anki_iterators import card_stream

instruction = """
First describe what aspects of the question are you answering,
then describe in full detail. 

"""

def handler(signum, frame):
    print("close after answering! by entering q")
signal.signal(signal.SIGTSTP, handler)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to the tsv Anki file", default='/home/a/Downloads/python.txt')
    parser.add_argument("--out", help="save session as JSONL", default="session.jsonl")
    parser.add_argument("--source", help="determine what source of question", default="anki", choices=['anki', 'file'])


    args = parser.parse_args()
    for card in card_stream(source=args.source, path=args.path):
        print(f"\n{instruction} \n\nquestion>{card.question}")
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
        print(f"<solution>{card.solution}</solution>")
        score = input("< = > ?")
        session = {
            "card_id": card.id,
            "question": card.question,
            "solution": card.solution,
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
