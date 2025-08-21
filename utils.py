
import sys


from dataclasses import dataclass


#one line of text from the input file
@dataclass
class Line:
    content: str
    number: int
    def startswith(self,txt,where=0):
        return self.content.startswith(txt,where)

#one section (slide)
@dataclass
class Section:
    title: str
    content: list[Line]


class OutputList:
    class Iterator:
        def __init__(self,owner):
            self.owner=owner
            self.i=0
        def __iter__(self):
            return self
        def __next__(self):
            if self.i == len(self.owner.data):
                raise StopIteration()
            tmp = self.owner.data[self.i]
            self.i+=1
            return tmp

    def __init__(self):
        self.data=[]
        self.indent=0

    def changeIndent(self,delta):
        self.indent += delta
        if self.indent < 0 :
            self.indent=0

    def append(self,*args):
        idx = len(self.data)
        tmp = " ".join(args)
        sp = "    "*self.indent
        self.data.append(sp+tmp)
        return idx

    def __setitem__(self,idx,value):
        assert type(value) == str
        self.data[idx] = value

    def __iter__(self):
        return OutputList.Iterator(self)


def error(*msg):
    t = [str(x) for x in msg]
    s = " ".join(t)
    print(s)
    sys.exit(1)


def warn(*msg):
    t = [str(x) for x in msg]
    s = " ".join(t)
    print(s)


def numLeadingSpaces(line:Line):
    ns=0
    for c in line.content:
        if c == ' ':
            ns+=1
        elif c == '\t':
            error("On line",line.number,": Leading tab character found; must use only spaces")
        else:
            return ns
    return ns
