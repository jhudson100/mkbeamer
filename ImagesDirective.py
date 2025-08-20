from Directive import DirectiveInfo, registerDirective
from utils import warn
import os.path

def imagesDirective(output,lines):

    spec = lines[0].content.strip()
    assert spec.startswith(".. images::")
    idx = spec.find("::")
    spec = spec[idx+2:].strip()
    lst = spec.split(",")
    width=0
    height=0
    altText=None

    output.append(r"\begin{center}")
    for item in lst:
        item=item.strip()
        litem = item.lower()
        if item.startswith("width="):
            i = item.find("=")
            #"canonical" size of screen is 1366x768;
            #latex doesn't use pixels, but existing slides
            #use that as a base for image size
            width = float( item[i+1:] )/1366
        elif item.startswith("height="):
            i = item.find("=")
            height = float( item[i+1:] )/768
        elif item.startswith("alt="):
            altText = item[4:].strip()
        elif litem.endswith(".svg") or litem.endswith(".jpg") or litem.endswith(".png"):
            filename = os.path.abspath(item)

            options=[]
            if width != 0:
                options.append("width={"+str(width)+r"\paperwidth}")
            if height != 0:
                #we scale everything with regard to the page width
                options.append("height={"+str(height)+"\paperwidth}")


            if not altText:
                warn("Image without alt text on line",lines[0].number)
            # ~ else:
                # ~ if not litem.endswith(".svg"):
                    # ~ options.append("alt={"+altText+"}")
                    # ~ #don't let alt text carry over to future files
                    # ~ altText=None

            if len(options):
                options = "["+",".join(options)+"]"

            if altText:
                output.append(r"\pdftooltip{")

            if litem.endswith(".svg"):
                #ref: https://tex.stackexchange.com/questions/740207/alt-text-for-svgs
                # ~ if altText:
                    # ~ output.append("{")
                    # ~ output.append(r"\setkeys{Gin}{alt="+altText+"}")
                output.append(r"\includesvg"+options+"{"+filename+"}%")
                # ~ if altText:
                    # ~ output.append("}")
                    # ~ #prevent carry over
                    # ~ altText=None
            else:

                output.append(r"\includegraphics"+options+"{"+filename+"}")
                # ~ if altText:
                    # ~ output.append(r"}{}")
                    # ~ altText=None

            if altText:
                output.append(r"}{"+altText+"}")

        else:
            error("Unknown item in images directive at line",lines[0].number,":",item)
    output.append(r"\end{center}")

    return DirectiveInfo(makeFragile=False)

registerDirective("images",imagesDirective)
