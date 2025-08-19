#!/usr/bin/env python3

#Q&D script...

import argparse
import sys
import re
from dataclasses import dataclass

@dataclass
class Section:
    title: str
    content: list[str]

#FIXME: Move this into a separate file
preamble=r"""\documentclass{beamer}
\title{%TITLE%}
\begin{document}
\frame{\titlepage}
"""


postamble=r"""
\end{document}
"""

def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument( "-o", dest="output", help="Output filename. Can also be specified as --output" )
    parser.add_argument( "--output", dest="output", help="Output filename. Can also be specified as -o")
    args = parser.parse_args(args)

    infile = args.filename
    outfile = args.output

    if outfile == None:
        if infile.endswith(".rst"):
            outfile = infile[:-4]+".tex"
        else:
            outfile = infile+".tex"

    print(infile,outfile)

    ofp = open(outfile,"w")


    with open(infile) as fp:
        inputLines = fp.readlines()

    slides = breakIntoSections(inputLines)

    tmp = preamble.replace("%TITLE%","title goes here")
    print(tmp,file=ofp)

    for slide in slides:
        print(r"\begin{frame}",file=ofp)
        print(r"\frametitle{",slide.title,"}",file=ofp)
        #FIXME: This is a stub
        print("CONTENT",file=ofp)
        print(r"\end{frame}",file=ofp)

    print(postamble,file=ofp)

    ofp.close()


def breakIntoSections(lines):
    underlinerex = re.compile(r"^={3,}[ \t]*$")
    sectionStarts=[]

    #find the location of slide title lines
    for i in range(2,len(lines)):
        potentialBlankLine = lines[i]
        if len(potentialBlankLine.strip()) == 0:
            potentialTitle = lines[i-2].rstrip()
            potentialUnderline = lines[i-1].rstrip()
            m = underlinerex.match(potentialUnderline)
            if m and len(m.group(0)) >= len(potentialTitle):
                sectionStarts.append( i-2 )

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
        #blank line is next line
        content = lines[ pair[0]+3:pair[1] ]
        sections.append(Section(title=title,content=content))

    return sections

main(sys.argv[1:])
