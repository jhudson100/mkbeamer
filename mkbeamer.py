#!/usr/bin/env python3

#TODO:
#   -> literals: `...`
#   -> attachments
#   -> tables
#   -> gap option in images directive
#   -> inline images
#   -> ordered lists
#   -> colors?
#   -> hyperlinks

import argparse
import sys
import re
from utils import Line, Section
import preamble
import section
import Directive
import os.path
import subprocess
import tempfile
import shutil

def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("filename",default="slides.rst",nargs='?')
    parser.add_argument( "-o","--output", dest="pdffile", help="Filename for PDF file. Can also be specified as -o")
    parser.add_argument( "--tex-output", dest="texfile", help="Store TeX to this filename. If omitted, a temporary file is used.")
    parser.add_argument( "--no-pdf", dest="no_pdf", action="store_true", help="Do not generate PDF file")
    parser.add_argument( "--once", dest="once", action="store_true", help="Only run XeLaTeX once")
    parser.add_argument( "--keep-temp", dest="keep_temp", action="store_true", help="Keep temporary folder (for debugging)")
    parser.add_argument( "-v","--verbose",dest="verbose", action="store_true",help="Verbose output")

    args = parser.parse_args(args)

    if args.keep_temp:
        tempdir = tempfile.mkdtemp()
        print("Using temporary directory",tempdir)
    else:
        #prevent garbage collection
        tempdirX = tempfile.TemporaryDirectory()
        tempdir = tempdirX.name

    infile = os.path.abspath(args.filename)

    texfile = os.path.join( tempdir, "out.tex" )

    if args.pdffile:
        pdffile = os.path.abspath(args.pdffile)
    else:
        if infile.endswith(".rst"):
            pdffile = infile[:-4]+".pdf"
        else:
            pdffile = infile+".pdf"


    docroot = os.path.dirname(infile)

    with open(infile) as fp:
        inputLines = fp.readlines()

    #break the input file up into separate slides (sections
    sections = breakIntoSections(inputLines)

    #The title of the first slide is the title of the presentation.
    #Content of the first slide is ignored
    title = sections[0].title
    for x in sections[0].content:
        if len(x.strip()):
            warn("Content of first slide will be discarded")
            break

    texfp = open( texfile,"w")
    print(preamble.getPreamble(title=title,docroot=docroot,tempdir=tempdir) , file=texfp)

    for slide in sections[1:]:
        tmp: list[str] = section.getContent(
            title=slide.title,
            lines=slide.content,
            docroot=docroot
        )
        for s in tmp:
            print(s,file=texfp)

    print(preamble.getPostamble(),file=texfp)

    texfp.close()

    if args.texfile:
        shutil.copyfile( os.path.join(tempdir,"out.tex"), args.texfile)

    #need to do twice to get page references correct
    #ref:https://tex.stackexchange.com/questions/149185/xelatex-quiet-output-and-halt-on-error
    #"-interaction=batchmode",
    if not args.no_pdf:

        #build pdf in temporary folder so we don't dump
        #intermediate files in the working directory
        os.chdir(tempdir)

        xelatex=["xelatex","-halt-on-error","-shell-escape","out.tex"]

        for i in range(2):
            if not args.once or i == 0:
                print("Running xelatex...")
                P = subprocess.Popen(xelatex,stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
                alltext=[]
                while True:
                    tmp = P.stdout.read(32)
                    if len(tmp) == 0:
                        break
                    tmp=tmp.decode()
                    alltext.append(tmp)
                    if args.verbose:
                        sys.stdout.write(tmp)
                        sys.stdout.flush()
                if P.returncode:
                    break
                analyzeOutput("".join(alltext),sections)
        else:
            shutil.copyfile( os.path.join(tempdir,"out.pdf"), pdffile )

    if args.keep_temp:
        print("Note: Temporary directory was not deleted:",tempdir)

overfullrex = re.compile(r"Overfull \\vbox [^\n]* at line (\d+)")
def analyzeOutput(output,sections):

    sliderex=re.compile(r"\[(\d+)\]")
    perSlideOutput=[]
    m = sliderex.search(output,0)
    while m:
        m2 = sliderex.search(output,m.end())
        perSlideOutput.append( output[ m.end():m2.start() if m2 else len(output) ] )
        m=m2

    for snum,so in enumerate(perSlideOutput):
        if overfullrex.search(so):
            firstline = sections[snum+1].content[0].number
            lastline = sections[snum+1].content[-1].number
            print("Slide",snum+2,"is overfull (input lines",firstline,"to",lastline,")")


    pagecountrex = re.compile(r"(?m)^Output written on [^(]+ \((\d+) page")
    m = pagecountrex.search(output)
    if m:
        print(m.group(1),"pages")




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
