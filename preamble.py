import os.path

MAXLISTDEPTH=9

def getPreamble(title, docroot):

    if not docroot.endswith(os.path.sep):
        docroot += os.path.sep
        
    with open(os.path.join(os.path.dirname(__file__),"preamble.tex")) as fp:
        preamble = fp.read()
        
    #ref: https://stackoverflow.com/questions/1935952/maximum-nesting-level-of-lists-in-latex
    tmp = [r"\usepackage{enumitem}"]
    for i in range(MAXLISTDEPTH):
        tmp.append(fr"\setlist[itemize,{i+1}]{{label=$\bullet$}}")
    tmp.append(fr"\renewlist{{itemize}}{{itemize}}{{ {MAXLISTDEPTH} }}")
    
    preamble = preamble.replace("%TITLE%",title)
    preamble = preamble.replace("%ENUMITEM%","\n".join(tmp))
    preamble = preamble.replace("%DOCROOT%",docroot)
    
    return preamble

def getPostamble():
    return r"""
\end{document}"""
