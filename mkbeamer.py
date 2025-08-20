#!/usr/bin/env python3

#TODO:
#   -> |item| substitutions
#   -> literals: `...`
#   -> math (inline, block)
#   -> sup, sub
#   -> attachments
#   -> tables
#   -> gap option in images directive
#   -> inline images

import argparse
import sys
import re
from utils import Line, Section
import preamble
import section
import Directive
import os.path
import subprocess

def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument( "-o", dest="output", help="Output filename. Can also be specified as --output" )
    parser.add_argument( "--output", dest="output", help="Output filename. Can also be specified as -o")
    parser.add_argument( "--no-minted",dest="no_minted",action="store_true", help="Do not use the 'minted' package for code blocks")

    args = parser.parse_args(args)

    infile = os.path.abspath(args.filename)
    outfile = os.path.abspath(args.output)

    docroot = os.path.dirname(infile)

    if args.no_minted:
        Directive.setUseMinted(False)

    if outfile == None:
        if infile.endswith(".rst"):
            outfile = infile[:-4]+".tex"
        else:
            outfile = infile+".tex"

    print(infile,outfile)

    ofp = open(outfile,"w")


    with open(infile) as fp:
        inputLines = fp.readlines()

    #break the input file up into separate slides (sections
    sections = breakIntoSections(inputLines)

    title = "FIXME:TITLE"

    print(preamble.getPreamble(title=title,docroot=docroot) , file=ofp)

    for slide in sections:
        tmp: list[str] = section.getContent(
            title=slide.title,
            lines=slide.content
        )
        for s in tmp:
            print(s,file=ofp)

    print(preamble.getPostamble(),file=ofp)

    ofp.close()

    os.chdir(os.path.dirname(outfile))
    #need to do twice to get page references correct

    #ref:https://tex.stackexchange.com/questions/149185/xelatex-quiet-output-and-halt-on-error
    #"-interaction=batchmode",
    xelatex=["xelatex","-halt-on-error","-shell-escape"]
    subprocess.check_call(xelatex+[outfile], stdin=subprocess.DEVNULL)
    subprocess.check_call(xelatex+[outfile], stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL)



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
        content = [ Line( content=lines[i], number=i+1 ) for i in range(pair[0]+3,pair[1])]
        #content = lines[ pair[0]+3:pair[1] ]
        sections.append(Section(title=title,content=content))

    return sections

main(sys.argv[1:])
