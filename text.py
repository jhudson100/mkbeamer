
from utils import Line
from Directive import testForInlineDirective, processInlineDirective

#output inline text, processing backslashes (\), pipes (|alpha|), and inline directives
def outputText(output: list[str], line: Line, docroot):
    i=0
    o=[]

    while i < len(line.content):
        c = line.content[i]
        if c == '\\':
            #next character is special:
            #   if space: Ignore it (for compat. with docutils)
            #   otherwise: output literally
            i+=1
            if i == len(line.content):
                error("On line",line.number,": Trailing backslash")
            if not line.content[i].isspace():
                o.append(line.content[i])
            i+=1
        elif c == '|':
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
                o.append(c)
                i+=1
        
    txt = "".join(o)
    output.append(txt)
