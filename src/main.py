import sys 

def parse_anki():
    path = '/home/a/Downloads/python.txt'

    with open(path) as f:
        for line in f.readlines():

            if '#' == line[0]:
                continue
            
            _, _, _, question, answer, _ = line.split('\t')
            print(f"q:{question} \n a:{answer}")
def main():
    print("Hello from my-cot!")


if __name__ == "__main__":
    parse_anki()
