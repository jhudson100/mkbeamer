
from utils import Line,error
from Directive import testForInlineDirective, processInlineDirective
import symbols
import re

hyperlinkrex=re.compile(r"`([^`]*)<([^>]+)>`__")

#ref: https://en.wikibooks.org/wiki/LaTeX/Special_Characters
specials={
    "<"     : r"{\textless}",
    ">"     : r"{\textgreater}",
    "%"     : r"{\%}",
    "_"     : r"{\_}",
    "|"     : r"{\textbar}",
    "#"     : r"{\#}",
    "&"     : r"{\&}",
    "{"     : r"{\{}",
    "}"     : r"{\}}",
    "~"     : r"\textasciitilde{}",
}
#output inline text, processing backslashes (\), pipes (|alpha|), and inline directives
def outputText(output: list[str], line: Line, docroot):
    i=0
    o=[]

    while i < len(line.content):
        if line.content.startswith("\\",i):
            #next character is special:
            #   if space: Ignore it (for compat. with docutils)
            #   otherwise: output literally
            i+=1
            if i == len(line.content):
                error("On line",line.number,": Trailing backslash")
            if not line.content[i].isspace():
                ch = line.content[i]
                ech = specials.get(ch,ch)
                o.append(ech)
            i+=1
        elif line.startswith("`",i):
            if line.startswith("``",i):
                #literal text
                assert 0,"FIXME: FINISH"
            else:
                #hyperlink:
                #`text to display<url>`__
                m = hyperlinkrex.match(line.content,i)
                if not m:
                    error("Bad hyperlink on line",line.number)
                display=m.group(1).strip()
                url=m.group(2).strip()
                if not display:
                    display=url
                o.append("\\href{"+url+"}{"+display+"}")
                i = m.end()
        elif line.startswith("**",i) or line.startswith("*",i) or line.startswith("__",i):
            if line.startswith("**",i):
                mode="textbf"
                j=i+2
                want="**"
            elif line.startswith("__",i):
                mode="underline"
                j=i+2
                want="__"
            else:
                mode="textit"
                j=i+1
                want="*"
            while j < len(line.content) and not line.content.startswith(want,j):
                j+=1
            if j == len(line.content):
                error(f"Unclosed {want} on line {line.number} (match for column {i})")
            txt = line.content[i+len(want):j]
            o.append("\\"+mode+"{")
            outputText(o,Line(number=line.number,content=txt),docroot)
            o.append("}")
            i = j+len(want)
        elif line.startswith("|",i):
            #fancy character
            i+=1
            j=i
            while True:
                if j == len(line.content):
                    error("On line",line.number,": Unpaired pipe (|)")
                if line.content[j] == '|':
                    break
                j+=1
            symbol = line.content[i:j]
            if symbol not in symbols.symbols:
                error(f"Unknown symbol '{symbol}' on line {line.number}")
            txt = symbols.symbols[symbol]
            o.append(txt)
            i = j+1
        else:
            m = testForInlineDirective(line, i )
            if m:
                i = processInlineDirective(o,line,m,docroot)
            else:
                ch = line.content[i]
                ech = specials.get(ch,ch)
                o.append(ech)
                i+=1

    txt = "".join(o)
    output.append(txt)
