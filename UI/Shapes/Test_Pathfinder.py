from pathlib import Path

p1 = Path('.')
p2 = Path('../')
p3 = Path(__file__)

path1 = p1.resolve()
path2 = p2.resolve()
path3 = p3.resolve().parents

print(path1)
print(path2)
print(f'\n')
root_dir = None
for parent in path3:
    if parent.name == 'BlenderDrawDev':
        root_dir = parent
        print('\t - Found it!')
    print(parent.name)

print(f'found root dir at:\n {root_dir}')


