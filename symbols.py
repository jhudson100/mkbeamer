symbolsstr = """
frac12  ½
rarr    →
larr    ←
forall  ∀
partial ∂
reg     ®
plusmn  ±
alpha   α
beta    β
gamma   γ
delta   δ
epsilon ε
"""

symbols = {}
for line in symbolsstr.strip().split("\n"):
    line = line.strip()
    key,val = line.split()
    symbols[key]=val
