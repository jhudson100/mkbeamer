

from utils import error, numLeadingSpaces
from dataclasses import dataclass
useMinted=True

@dataclass
class DirectiveInfo:
    makeFragile: bool

def setUseMinted(flag:bool):
    global useMinted
    useMinted=flag

directiveHandlers={}
def registerDirective(name, handler):
    if name in directiveHandlers and directiveHandlers[name] != handler:
        raise RuntimeError(f"Duplicate directive: {name}")
    directiveHandlers[name]=handler


import CodeDirective
import ImagesDirective


def process(output, directiveName, directiveContent) -> DirectiveInfo:
    if directiveName in directiveHandlers:
        return directiveHandlers[directiveName](output,directiveContent)
    else:
        error(f"Unknown directive '{directiveName}' on line {directiveContent[0].number}")


def handleBlockDirective(output,lines,i):
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
    directiveInfo = process(output,directiveName,directiveContent)
    return j, directiveInfo.makeFragile
