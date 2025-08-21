

from utils import error, numLeadingSpaces,Line
from dataclasses import dataclass
import re

@dataclass
class DirectiveInfo:
    makeFragile: bool

blockHandlers={}
def registerBlockDirective(name, handler):
    if name in blockHandlers and blockHandlers[name] != handler:
        raise RuntimeError(f"Duplicate directive: {name}")
    blockHandlers[name]=handler

inlineHandlers={}
def registerInlineDirective(name, handler):
    if name in inlineHandlers and inlineHandlers[name] != handler:
        raise RuntimeError(f"Duplicate directive: {name}")
    inlineHandlers[name]=handler


inlineRex = re.compile(r"(?m):([a-z]+):`(\\`|[^`])+`")

def testForInlineDirective(line,i):
    if i == 0 or line.content[i-1].isspace():
        m = inlineRex.match( line.content,i )
        return m
    else:
        return None

def processInlineDirective(output, line, matchObject: re.Match, docroot) -> None:
    directiveName = matchObject.group(1)
    directiveContent = matchObject.group(2)
    if directiveName in inlineHandlers:
        inlineHandlers[directiveName](output=output,line=line,directiveName=directiveName,directiveContent=directiveContent,docroot=docroot)
    else:
        error(f"Unknown inline directive '{directiveName}' on line {line.number}")

    return matchObject.end()
 

def handleBlockDirective(output,lines,i,docroot):
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

    if directiveName in blockHandlers:
        directiveInfo = blockHandlers[directiveName](output=output,directiveContent=directiveContent,docroot=docroot)
    else:
        error(f"Unknown block directive '{directiveName}' on line {directiveContent[0].number}")


    return j, directiveInfo.makeFragile




import CodeDirective
import ImagesDirective
import SuperSubDirective
import RawDirective
