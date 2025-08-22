from utils import error, numLeadingSpaces,Line,OutputList
import re
import text

listItemRex = re.compile(r"\s*\*\s")

def matches(line:Line):
    return listItemRex.match(line.content)
        
def process(output: list[str], lines: list[Line], i: int, docroot:str):

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
