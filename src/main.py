import os
import sys
import graphviz
from html.parser import HTMLParser

class HyperlinkParser(HTMLParser):
    hyperlink = None
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.hyperlink = attrs[0][1]
        else:
            self.hyperlink = None

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py directory")
        exit(1)
    if sys.argv[1][-1] == "/":
        rootdir = sys.argv[1][0:-1]
    else:
        rootdir = sys.argv[1]
    paths = generate_paths(rootdir)
    #for i in paths:
        #print(i)
    
    parser = HyperlinkParser()
    digraph = graphviz.Digraph(renderer="cairo", format="svg", graph_attr={"concentrate": "true"}, strict=True)
    for i in paths:
        digraph.node(i, i)

    edges = set()
    for file in paths:
        fd = open(file, "r")
        for line in fd:
            parser.feed(line)
            print(parser.hyperlink)
            if parser.hyperlink != None:
                #print(parser.hyperlink, file)
                for target in paths:
                    if "milocraun.com/" + parser.hyperlink == target and file != target:
                        edges.add((file, "milocraun.com/" + parser.hyperlink))
        fd.close()


    for element in edges:
        digraph.edge(element[0], element[1])
    digraph.render(outfile=rootdir + "-graph.svg")

def generate_paths(path):
    walk = os.walk(path)
    file = list()
    for entry in walk:
        for filename in entry[2]:
            if ".html" in filename:
                print(entry[0], filename)
                if entry[0][:-1] == "/":
                    file.append(entry[0] + filename)
                else:
                    file.append(entry[0] + "/" + filename)
    return file;

if __name__ == "__main__":
    main()
