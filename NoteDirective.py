
from Directive import registerInlineDirective, registerBlockDirective, DirectiveInfo
from text import outputText
from utils import Line

    
def block(output,directiveContent,docroot) -> DirectiveInfo:
    print("FIXME: WE HAVE A NOTE")
    idx = directiveContent[0].content.find("::")
    assert idx != -1
    print(directiveContent[0].content[idx+2:])
    i=1
    while i < len(directiveContent) and directiveContent[i].content.strip() == "":
        i+=1
    for line in directiveContent[i:]:
        c = line.content.strip()
        print("FIXME:",c)
        
    return DirectiveInfo(makeFragile=False)
    

registerBlockDirective("note",block)


