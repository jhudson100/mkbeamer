
from Directive import registerInlineDirective, registerBlockDirective, DirectiveInfo
from text import outputText
from utils import Line

def rawInline(output,line,directiveName,directiveContent,docroot):
    output.append(directiveContent)
    
def rawBlock(output,directiveContent,docroot) -> DirectiveInfo:
    i = 1
    while i < len(directiveContent) and directiveContent[i].content.strip() == "":
        i+=1
    for line in directiveContent[i:]:
        output.append(line.content)
    return DirectiveInfo(makeFragile=True)
    

registerInlineDirective("raw",rawInline)
registerBlockDirective("raw",rawBlock)


