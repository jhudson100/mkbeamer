from utils import error, numLeadingSpaces,Line,OutputList,TreeNode
import re
import text

listItemRex = re.compile(r"\s*\*\s")

class ListNode(NonleafNode):
    pass

class ListItemNode(NonleafNode):
    pass
    
def matches(line:Line):
    return listItemRex.match(line.content)

itemRex = re.compile(r" *\* ")
def indentationLevel(line: Line) -> int:
    if not itemRex.match(line):
        error("Expected a list item, but did not get one")
    sp = numLeadingSpaces(line)
    if sp % 4:
        error("List indentation: Not a multiple of 4 spaces on line", line.number)
    return sp/4

def process(lines: LineList, docroot:str) -> TreeNode:

    nestingLevel = indentationLevel(lines[i])
    listNode = ListNode()
    
    while i < len(lines):
        if not listItemRex.match( lines.peek().content ):
            #end of the list
            break
        nl = nestingLevel( lines.peek() )
        if nl > nestingLevel:
            #nested list
            sublist = process(lines,docroot)
            listNode.addChild(sublist)
        elif nl == nestingLevel:
            line = lines.next()
            listNode.addChild(text.process(line,docroot))
        else:
            #nl < nestingLevel
            #done with this list
            break

    return listNode
    
            # ~ output.append(r"\begin{itemize}")
            # ~ output.changeIndent(1)
            # ~ nestingLevel+=1
        # ~ while nl < nestingLevel:
            # ~ output.changeIndent(-1)
            # ~ output.append(r"\end{itemize}")
            # ~ nestingLevel-=1

        # ~ tmp = lines[i].content.strip()
        # ~ assert tmp.startswith("*")
        # ~ #remove the leading bullet
        # ~ tmp = tmp[1:]
        # ~ #remove any spaces after the bullet
        # ~ tmp = tmp.lstrip()

        # ~ newitem = Line(number=lines[i].number, content=tmp )

        # ~ output.append(r"\item ")
        # ~ output.changeIndent(1)
        # ~ text.outputText(output,newitem,docroot)
        # ~ output.changeIndent(-1)
        # ~ i+=1

    # ~ while nestingLevel > -1:
        # ~ output.changeIndent(-1)
        # ~ output.append(r"\end{itemize}")
        # ~ nestingLevel-=1

    # ~ return i
