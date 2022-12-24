import os
import sys


def main():
    if len(sys.argv) != 2:
        exit(1)
    paths = generate_paths(sys.argv[1])
    for i in paths:
        print(i)

def generate_paths(path):
    walk = os.walk(path)
    file = list()
    for entry in walk:
        for filename in entry[2]:
            file.append(entry[0] + "/" + filename)
    return file;

if __name__ == "__main__":
    main()
