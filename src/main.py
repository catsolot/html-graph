import os
import sys
import graphviz
from html.parser import HTMLParser

class HyperlinkParser(HTMLParser):
    data = None
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.data = attrs[0][1]
        else:
            self.data = None

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py directory")
        print("Please do not include a trailing / after directory")
        exit(1)
    #if sys.argv[1][-1] == "/":
    #    paths = generate_paths(sys.argv[1][0:-1])
    #else:
    #    paths = generate_paths(sys.argv[1])
    paths = generate_paths(sys.argv[1])
    for i in paths:
        print(i)
    
    parser = HyperlinkParser()
    digraph = graphviz.Digraph(renderer="cairo", format="svg", graph_attr={"concentrate": "true"}, strict=True)
    for i in paths:
        digraph.node(i, i)

    edges = set()
    for file in paths:
        f = open(file, "r")
        for line in f:
            parser.feed(line)
            if parser.data != None:
                for i in paths:
                    if "milocraun.com/" + parser.data == i and file != i:
                        edges.add((file, "milocraun.com/" + parser.data))
        f.close()

    for element in edges:
        digraph.edge(element[0], element[1])
    digraph.render(outfile=sys.argv[1] + "-graph.svg")

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
