

from utils import error, numLeadingSpaces
from  dataclasses import dataclass

useMinted=True

@dataclass
class DirectiveInfo:
    makeFragile: bool

def setUseMinted(flag:bool):
    global useMinted
    useMinted=flag
    
directiveHandlers={}
def registerDirective(name, handler):
    if name in directiveHandlers:
        raise RuntimeError(f"Duplicate directive: {name}")
    directiveHandlers[name]=handler
    
def process(output, directiveName, directiveContent) -> DirectiveInfo:
    if directiveName in directiveHandlers:
        return directiveHandlers[directiveName](output,directiveContent)
    else:
        error(f"Unknown directive '{directiveName}' on line {directiveContent[0].number}")

def codeDirective(output,lines) -> DirectiveInfo:

    tmp = lines[0].content.split()
    # .. code:: python
    if len(tmp) < 3:
        lang="text"
    else:
        lang = tmp[2]

    size=100
    
    i=1
    while len(lines[i].content.strip()) > 0:
        tmp = lines[i].content.strip()
        if tmp.startswith(":class:"):
            tmp = tmp.split()
            if len(tmp) != 2:
                error("Bad class for code directive at line",lines[i].number)
            klass = tmp[1]
            if klass.startswith("size"):
                size=int(klass[4:])
        else:
            error("Unknown modifier for code directive at line",lines[i].number,":",tmp)
        
        i=i+1
        
    #we should now be sitting at a blank linke

    #size for 100%, in points
    size100 = 11
    
    if useMinted:
        #tcbox=fitted, tcolorbox=full page width
        output.append(r"\begin{tcolorbox}[colback=white,colframe=black]%")
        fsize = size100 * size/100
        spacing = fsize * 1.1
        output.append(r"\fontsize{"+str(fsize)+"pt}{"+str(spacing)+"pt}\selectfont")
        output.append(r"\begin{minted}[bgcolor=white,breaklines=true]{c}")
    else:
        output.append(r"\begin{verbatim}")
    
    #find the minimum indent of anything in content
    #and remove that many items
    print(lines)
    minIndent = min( [ numLeadingSpaces(line) for line in filter(lambda s: len(s.content.strip())>0, lines[1:]) ] )

    print("mindent=",minIndent)
    
    #skip leading blank lines
    while i < len(lines):
        if len(lines[i].content.strip()) != 0:
            break
        else:
            i+=1

    #skip trailing blank lines
    j = len(lines)-1
    while j > i:
        if len(lines[j].content.strip()) != 0:
            break
        else:
            j=j-1

    for line in lines[i:j+1]:
        output.append( line.content[minIndent:].rstrip() )

    if useMinted:
        output.append(r"\end{minted}")
        output.append(r"\end{tcolorbox}")
    else:
        output.append(r"\end{verbatim}")
        
    return DirectiveInfo(makeFragile=True)
        
def imagesDirective(output,lines):

    spec = lines[0].content.strip()
    assert spec.startswith(".. images::")
    idx = spec.find("::")
    spec = spec[idx+2:].strip()
    lst = spec.split(",")
    width=0
    height=0
    output.append(r"\begin{center}")
    for item in lst:
        item=item.strip()
        if item.startswith("width="):
            i = item.find("=")
            #"canonical" size of screen is 1366x768;
            #latex doesn't use pixels, but existing slides
            #use that as a base for image size
            width = float( item[i+1:] )/1366
        elif item.startswith("height="):
            i = item.find("=")
            height = float( item[i+1:] )/768
        elif item.lower().endswith(".svg"):
            options=[]
            if width != 0:
                options.append("width={"+str(width)+r"\paperwidth}")
            if height != 0:
                #we scale everything with regard to the page width
                options.append("height={"+str(height)+"\paperwidth}")
            if len(options):
                options = "["+",".join(options)+"]"
            output.append(r"\includesvg"+options+"{"+item+"}")
        elif item.lower().endswith(".jpg"):
            pass
        elif item.lower().endswith(".png"):
            pass
        else:
            error("Unknown item in images directive at line",lines[0].number,":",item)
    output.append(r"\end{center}")
    
    return DirectiveInfo(makeFragile=False)

registerDirective("code",codeDirective)
registerDirective("images",imagesDirective)
