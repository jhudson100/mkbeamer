import re
from utils import error, numLeadingSpaces,Line,OutputList
import Directive

listItemRex = re.compile(r"\s*\*\s")

def getContent(title: str,lines: list[Line]) -> list[str]:
    output = OutputList()

    idx = output.append(r"\begin{frame}")
    output.append(r"\frametitle{",title,"}")

    makeFragile=False
    i = 0
    while i < len(lines):
        if 0 == len(lines[i].content.strip()):
            i += 1
        elif listItemRex.match(lines[i].content):
            i = parseList(output,lines,i)
        elif lines[i].content.startswith(".. "):
            i,mf = Directive.handleBlockDirective(output,lines,i)
            if mf:
                makeFragile=True
        else:
            error("Unknown slide content on line",lines[i].number,":",lines[i].content)

    if makeFragile:
        output[idx] = r"\begin{frame}[fragile]"

    output.append(r"\end{frame}")
    return output

inlineRex = re.compile(r":(sup|sub|math|attach):`(\\`|[^`])+`")

def outputText(output: list[str], line: Line):
    i=0
    o=[]

    while i < len(line.content):
        c = line.content[i]
        if c == '\\':
            #next character is taken literally
            i+=1
            if i == len(line.content):
                error("On line",line.number,": Trailing backslash")
            o.append(line.content[i])
            i+=1
        elif c == '|':
            #fancy character
            i+=1
            j=i
            while True:
                if j == len(line.content):
                    error("On line",line.number,": Unpaired pipe (|)")
                if line.content[j] == '|':
                    break
                j+=1
            symbol = line.content[i:j]
            assert 0, "FIXME: INSERT SYMBOL"
            i = j+1
        else:
            m = inlineRex.match( line.content,i )
            if m:
                command = m.group(1)
                assert 0
                i=m.end()+1
            else:
                o.append(c)
                i+=1

    txt = "".join(o)
    output.append(txt)




def parseList(output: list[str], lines: list[Line], i: int):

    nestingLevel=-1

    while i < len(lines) and listItemRex.match( lines[i].content ):
        line = lines[i]
        sp = numLeadingSpaces(line)
        if sp % 4:
            error("List indentation: Not a multiple of 4 spaces on line", line.number)
        nl = sp/4
        while nl > nestingLevel:
            output.append(r"\begin{itemize}")
            output.changeIndent(1)
            nestingLevel+=1
        while nl < nestingLevel:
            output.changeIndent(-1)
            output.append(r"\end{itemize}")
            nestingLevel-=1

        tmp = lines[i].content.strip()
        assert tmp.startswith("*")
        #remove the leading bullet
        tmp = tmp[1:]
        #remove any spaces after the bullet
        tmp = tmp.lstrip()

        newitem = Line(number=lines[i].number, content=tmp )

        output.append(r"\item ")
        output.changeIndent(1)
        outputText(output,newitem)
        output.changeIndent(-1)
        i+=1

    while nestingLevel > -1:
        output.changeIndent(-1)
        output.append(r"\end{itemize}")
        nestingLevel-=1

    return i
