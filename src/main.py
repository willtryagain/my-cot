import sys 
from datetime import datetime
import json
import os 
import signal 
import argparse
instruction = """
First describe what aspects of the question are you answering,
then describe in full detail. 

"""

def handler(signum, frame):
    print("close after answering! by entering q")
signal.signal(signal.SIGTSTP, handler)


def iter_anki(input='/home/a/Downloads/python.txt'):
    with open(input) as f:
        for line in f.readlines():

            if '#' == line[0] or len(line.split('\t')) != 6:
                continue
            
            card_id, _, _, question, solution, _ = line.split('\t')
            yield card_id, question, solution 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path to the tsv Anki file", default='/home/a/Downloads/python.txt')
    parser.add_argument("--out", help="save session as JSONL", default="session.jsonl")
    args = parser.parse_args()
    for card_id, question, solution in iter_anki(args.input):
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
