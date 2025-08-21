
from Directive import registerInlineDirective, registerBlockDirective, DirectiveInfo
from text import outputText
from utils import Line

def inline(output,line,directiveName,directiveContent,docroot):
    output.append("\\begin{math}")
    output.append(directiveContent)
    output.append("\\end{math}")
    
    
def block(output,directiveContent,docroot) -> DirectiveInfo:
    output.append("\\begin{displaymath}")
    i = 1
    while i < len(directiveContent) and directiveContent[i].content.strip() == "":
        i+=1
    for line in directiveContent[i:]:
        c = line.content.strip()

        #we can't have empty lines in displaymath
        if len(c) > 0:
            output.append(c)
            
    output.append("\\end{displaymath}")
    return DirectiveInfo(makeFragile=True)
    

registerInlineDirective("math",inline)
registerBlockDirective("math",block)


