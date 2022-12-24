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
    digraph.attr("graph", concentrate="true")
    digraph.strict = True
    for i in paths:
        digraph.node(i, i)

    edges = set()
    for file in paths:
        f = open(file, "r")
        for line in f:
            if "<a " in line:
                start_pos = line.find("href=")
                end_pos = line.find('"', start_pos + 6)
                val = line[start_pos+6:end_pos]
                val = "milocraun.com/" + val
                for i in paths:
                    print(val, i)
                    if val == i:
                        edges.add((file, val))
                        
    print(edges)
    for element in edges:
        digraph.edge(element[0], element[1])
    f.close()
    digraph.render()


def generate_paths(path):
    walk = os.walk(path)
    file = list()
    for entry in walk:
        for filename in entry[2]:
            if ".html" in filename:
                if entry[0][:-1] == "/":
                    file.append(entry[0] + filename)
                else:
                    file.append(entry[0] + "/" + filename)
    return file;

if __name__ == "__main__":
    main()
