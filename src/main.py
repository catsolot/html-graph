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
    paths = generate_paths(sys.argv[1])
    for i in paths:
        print(i)
    
    parser = HyperlinkParser()
    digraph = graphviz.Digraph()
    digraph.renderer = "cairo"
    digraph.format = "svg"
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
        f.close()
                        


    edges2 = set()
    for file in paths:
        f = open(file, "r")
        for line in f:
            parser.feed(line)
            if parser.data != None:
                for i in paths:
                    if "milocraun.com/" + parser.data == i:
                        edges2.add((file, "milocraun.com/" + parser.data))
        f.close()
    for i in edges2:
        print(i)

    print("\n")
    for i in edges:
        print(i)


    for element in edges2:
        digraph.edge(element[0], element[1])
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
