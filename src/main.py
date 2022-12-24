import os
import sys
import graphviz


def main():
    if len(sys.argv) != 2:
        exit(1)
    paths = generate_paths(sys.argv[1])
    for i in paths:
        print(i)
    
    digraph = graphviz.Digraph()
    digraph.renderer = "cairo"
    digraph.format = "png"
    for i in paths:
        digraph.node(i, i)

    for file in paths:
        f = open(file, "r")
        lines = f.readlines()
        for l in lines:
            for i in paths:
                if l.strip() in i:
                    digraph.edge(file, i) 
        f.close()
    print(digraph.body) 
    digraph.render()


def generate_paths(path):
    walk = os.walk(path)
    file = list()
    for entry in walk:
        for filename in entry[2]:
            if ".html" in filename:
                file.append(entry[0] + "/" + filename)
    return file;

if __name__ == "__main__":
    main()
