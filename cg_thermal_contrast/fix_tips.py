"""Set the numbers in the hover tips (Section/Theorem/... N:) from the .aux file of the last compilation."""
import re, sys
tex, aux = sys.argv[1], sys.argv[2]
num = {}
for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', open(aux).read()):
    num[m.group(1)] = m.group(2)
s = open(tex).read()
head, tail = s.split('\n\\end{document}\n', 1)
cnt = 0
def fix(m):
    global cnt
    lab, kind, old = m.group(1), m.group(2), m.group(3)
    new = num.get(lab, old)
    if new != old:
        cnt += 1
    return m.group(0).replace(kind + ' ' + old + ':', kind + ' ' + new + ':', 1)
head = re.sub(r'\\csname CGTip@([^\\]+)\\endcsname\{(Section|Theorem|Proposition|Lemma|Corollary|Table|Figure) ([0-9.]+):', fix, head)
open(tex, 'w').write(head + '\n\\end{document}\n' + tail)
print('tips renumbered:', cnt)
