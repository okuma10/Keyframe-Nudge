from pathlib import Path

p1 = Path('.')
p2 = Path('../')
p3 = Path(__file__).parent

path1 = p1.resolve()
path2 = p2.resolve()
# path3 = p3.resolve().parents

print(p3)

