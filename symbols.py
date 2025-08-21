symbolsstr = """
frac12      ½
rarr        →
larr        ←
forall      ∀
partial     ∂
reg         ®
plusmn      ±
infinity    ∞
infin       ∞
radic       √
cap         ∩
cup         ∪
asymp       ≈
isin        ∊
sdot        ∙
times       ×
divide      ÷
alpha       α
beta        β
gamma       γ
delta       δ
epsilon     ε
Omega       Ω
"""

symbols = {}
for line in symbolsstr.strip().split("\n"):
    line = line.strip()
    key,val = line.split()
    symbols[key]=val
