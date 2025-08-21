
from Directive import registerInlineDirective
from text import outputText
from utils import Line

def supsubHandler(output,line,directiveName,directiveContent,docroot):
    if directiveName == "sup":
        d = "\\textsuperscript"
    else:
        d = "\\textsubscript"
    output.append(d+"{")
    outputText(output,Line(number=line.number,content=directiveContent),docroot=docroot )
    output.append("}")
    

registerInlineDirective("sup",supsubHandler)
registerInlineDirective("sub",supsubHandler)


