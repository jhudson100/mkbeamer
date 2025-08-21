import re
from utils import error, numLeadingSpaces,Line,OutputList
import Directive
import symbols
import text

listItemRex = re.compile(r"\s*\*\s")

def getContent(title: str,lines: list[Line], docroot: str) -> list[str]:
    output = OutputList()

    idx = output.append(r"\begin{frame}")
    output.append(r"\frametitle{",title,"}")

    makeFragile=False
    i = 0
    while i < len(lines):
        if 0 == len(lines[i].content.strip()):
            i += 1
        elif listItemRex.match(lines[i].content):
            i = parseList(output=output,lines=lines,i=i,docroot=docroot)
        elif lines[i].content.startswith(".. "):
            i,mf = Directive.handleBlockDirective(output=output,lines=lines,i=i,docroot=docroot)
            if mf:
                makeFragile=True
        else:
            error("Unknown slide content on line",lines[i].number,":",lines[i].content)

    if makeFragile:
        output[idx] = r"\begin{frame}[fragile]"

    output.append(r"\end{frame}")
    return output

inlineRex = re.compile(r":[a-z]+:`(\\`|[^`])+`")




def parseList(output: list[str], lines: list[Line], i: int, docroot:str):

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
        text.outputText(output,newitem,docroot)
        output.changeIndent(-1)
        i+=1

    while nestingLevel > -1:
        output.changeIndent(-1)
        output.append(r"\end{itemize}")
        nestingLevel-=1

    return i
