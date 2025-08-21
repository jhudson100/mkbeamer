from Directive import DirectiveInfo, registerBlockDirective
from utils import numLeadingSpaces

useMinted=True

def codeDirective(output,directiveContent,docroot) -> DirectiveInfo:

    lines = directiveContent
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
        output.append(r"\begin{tcolorbox}[colback=white,colframe=black,boxsep=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt]%")
        fsize = size100 * size/100
        spacing = fsize * 1.1
        output.append(r"\fontsize{"+str(fsize)+"pt}{"+str(spacing)+"pt}\selectfont")
        output.append(r"\begin{minted}[bgcolor=white,breaklines=true]{c}")
    else:
        output.append(r"\begin{verbatim}")

    #find the minimum indent of anything in content
    #and remove that many items
    minIndent = min( [ numLeadingSpaces(line) for line in filter(lambda s: len(s.content.strip())>0, lines[1:]) ] )


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

registerBlockDirective("code",codeDirective)
