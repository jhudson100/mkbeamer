#todo: See https://tex.stackexchange.com/questions/313736/in-beamer-whats-the-right-way-to-scale-a-slide-element-down-to-better-fit

import re
from utils import error, numLeadingSpaces,Line,OutputList,Section
import Directive
import symbols
import UnorderedList

sectionOptions=set(["scale"])

def getContent(section: Section, docroot:str) -> list[str]:
    title=section.title
    lines=section.content
    options=section.options
    for key in options:
        if key not in sectionOptions:
            error(f"Unknown option '{key}' for section at line",section.firstLine)

    output = OutputList()

    idx = output.append(r"\begin{frame}")

    # ~ output.append(r"\BeginAccSupp{method=escape,unicode,ActualText=FIXME}")

    output.append(r"\frametitle{",title,"}")

    if "scale" in options:
        amt = float(options["scale"])
        #ref: https://tex.stackexchange.com/questions/313736/in-beamer-whats-the-right-way-to-scale-a-slide-element-down-to-better-fit
        #ref: https://tex.stackexchange.com/questions/67843/problem-resizing-an-itemize-environment-with-a-scalebox-somethings-wrong
        output.append(r"\scalebox{"+str(amt)+"}{")
        output.append(r"\vbox{")

    makeFragile=False
    i = 0
    while i < len(lines):
        if 0 == len(lines[i].content.strip()):
            i += 1
        elif UnorderedList.matches(lines[i]):
            i = UnorderedList.process(output=output,lines=lines,i=i,docroot=docroot)
        elif lines[i].content.startswith(".. "):
            tmp = Directive.handleBlockDirective(output=output,lines=lines,i=i,docroot=docroot)

            i,mf = tmp
            if mf:
                makeFragile=True
        else:
            error("Unknown slide content on line",lines[i].number,":",lines[i].content)

    if "scale" in options:
        output.append("} %vbox")
        output.append("} %scalebox")

    # ~ output.append(r"\EndAccSupp{}")

    output.append(r"\end{frame}")

    if makeFragile:
        output[idx] = r"\begin{frame}[fragile]"

    return output



def split(lines):

    #at least three underlines AND enough underlines to be longer
    #than preceding line length; options specified in bracket group
    #ex:
    #   Title
    #   =========[scale=0.8]

    underlinerex = re.compile(r"^(={3,})(\[([^]]*)\])?[ \t]*$")
    sectionStarts=[]

    #find the location of slide title lines
    for i in range(2,len(lines)):
        potentialBlankLine = lines[i]
        if len(potentialBlankLine.strip()) == 0:
            potentialTitle = lines[i-2].rstrip()
            potentialUnderline = lines[i-1].rstrip()
            m = underlinerex.match(potentialUnderline)
            if m and len(m.group(1)) >= len(potentialTitle):
                sectionStarts.append( i-2  )

    #make list of slide start/end locations
    sectionRanges=[]
    start=0
    for end in sectionStarts:
        sectionRanges.append( [start,end] )
        start=end
    sectionRanges.append( [start,len(lines)] )

    #trim off leading or trailing blank lines
    for pair in sectionRanges:
        while pair[0] < pair[1] and len( lines[pair[0]].strip()) == 0:
            pair[0]+=1
        while pair[1] > pair[0] and len(lines[pair[1]-1].strip()) == 0:
            pair[1]-=1

    sections=[]
    for pair in sectionRanges:
        if pair[0] >= pair[1]:
            continue
        title = lines[pair[0]].strip()
        #underline is next line
        underline=lines[pair[0]+1].strip()
        m = underlinerex.match(underline)
        if not m:
            assert 0,f"line {pair[0]+1}: {underline}"
        options={}
        if m.group(3):
            for opt in m.group(3).split(","):
                opt=opt.strip()
                key,value=opt.split("=")
                options[key]=value


        #blank line is next line

        firstLine=pair[0]
        lastLine=pair[1]
        content = [ Line( content=lines[i], number=i+1 ) for i in range(firstLine+3,lastLine)]
        #content = lines[ pair[0]+3:pair[1] ]
        sections.append(Section(title=title,content=content,options=options,
            firstLine=firstLine,lastLine=lastLine))

    return sections


# ~ inlineRex = re.compile(r":[a-z]+:`(\\`|[^`])+`")
