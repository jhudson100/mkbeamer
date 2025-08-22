
import sys


from dataclasses import dataclass

class TreeNode:
    def __init__(self):
        pass
    def walk(self,precallback=None,postcallback=None):
        try:
            self._walk(precallback,postcallback)
        except StopIteration:
            pass
    def _walk(self,precallback,postcallback):
        assert 0
        
    def getChildren(self) -> list[TreeNode]:
        assert 0
        
class LeafNode(TreeNode):
    def __init__(self):
        pass
    def getChildren(self):
        return []
    def _walk(self,precallback,postcallback):
        if precallback:
            precallback(self)
        if postcallback:
            postcallback(self)

#node's children are fixed at creation time;
#cannot add arbitrary number of children
class SemileafNode(TreeNode):
    def __init__(self):
        self.children=[]
    def getChildren(self):
        return self.children
    def _walk(self,precallback,postcallback):
        if precallback:
            precallback(self)
        for c in self.getChildren():
            c.walk(style,precallback=precallback,postcallback=postcallback)
        if postcallback:
            postcallback(self)
    
class NonleafNode(FixedChildNode):
    def __init__(self):
        super().__init__()
    def addChild(self, n: TreeNode):
        self.children.append(n)
        
class LineList:
    def __init__(self,lines):
        self.lines=lines
        self.i=0
    def peek(self):
        if self.i == len(self.lines):
            return None
        return self.lines[self.i]
    def next(self):
        if self.i == len(self.lines):
            return None
        t = self.lines[self.i]
        self.i+=1
        return t
        
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
    options: dict[str,str]
    firstLine: int
    lastLine: int


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
