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
            i,mf = parseBlockDirective(output,lines,i)
            if mf:
                makeFragile=True
        else:
            error("Unknown slide content on line",lines[i].number,":",lines[i].content)

    if makeFragile:
        output[idx] = r"\begin{frame}[fragile]" 
            
    output.append(r"\end{frame}")
    return output

def parseBlockDirective(output,lines,i):
    assert lines[i].content.startswith(".. ")

    #if the first word after the ..'s ends with a colon, this is a directive
    #otherwise, it's a comment
    tmp = lines[i].content.split()
    if len(tmp) == 1:
        #no directive; just a comment
        return i+1
    if not tmp[1].endswith("::") :
        #warn about potential typo
        if tmp[2].endswith(":"):
            warn("On line",lines[i].number,": Possible mistyped directive? Ignoring...")
        return i+1

    directiveName = tmp[1][:-2]

    
    j=i+1
    
    #include any indented and/or blank lines
    while j < len(lines):
        if len(lines[j].content.strip()) == 0 or lines[j].content.startswith(" "):
            j+=1
        else:
            #end of file or unindented line
            break

    #directive content goes from i to j-1 inclusive
    directiveContent = lines[i:j]
    directiveInfo = Directive.process(output,directiveName,directiveContent)
    return j, directiveInfo.makeFragile

    

def outputText(output: OutputList, line: Line):
    output.append( line.content )
    
    
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
        #remove the leading bullet
        tmp = tmp[1:]
        #remove any spaces after the bullet
        tmp = tmp.lstrip()

        output.append(r"\item ")
        output.changeIndent(1)
        outputText(output,Line(number=line.number,content=tmp))
        output.changeIndent(-1)
        i+=1

    while nestingLevel > -1:
        output.changeIndent(-1)
        output.append(r"\end{itemize}")
        nestingLevel-=1

    return i
        
        



    
