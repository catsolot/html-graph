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
            #print(parser.hyperlink)
            if parser.hyperlink != None:
                #print(parser.hyperlink, file)
                link = handle_link(parser.hyperlink, file)
                name = rootdir + "/" + link
                print(name)
                if name in paths and file != name:
                    
                    #print("Hyperlink: {} Target: {} File: {}".format(parser.hyperlink, name, file) )
                    edges.add((file, name))
               # for target in paths:
               #     # TODO: Fix parsing for subdirectories
               #     # if we find .. then we want to substitute it for
               #     # the directory directly above.
               #     print("Hyperlink: {} Target: {} File: {}".format(parser.hyperlink, target, file) )
        fd.close()

    #print(edges)

    for element in edges:
        digraph.edge(element[0], element[1])
    digraph.render(outfile=rootdir + "-graph.svg")

def generate_paths(path):
    walk = os.walk(path)
    file = list()
    for entry in walk:
        for filename in entry[2]:
            if ".html" in filename:
                #print(entry[0], filename)
                if entry[0][:-1] == "/":
                    file.append(entry[0] + filename)
                else:
                    file.append(entry[0] + "/" + filename)
    return file;

def handle_link(link, path):
    #print(link)
    #print(link, path)
    num = link.count("../")
    if num == 0:
        return link
    sp = path.split("/")
    li = link.split("/")
    lin = li.pop()
    fi = sp.pop()
    sp.pop(0)
    for i in range(num):
        sp.pop()
    res = ""
    for i in sp:
        res = res + i + "/"
    res = res + lin 
    print(res)
    return res


if __name__ == "__main__":
    main()
