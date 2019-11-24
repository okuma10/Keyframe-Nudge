from pathlib import Path

parents = Path(__file__).parents
UI_dir = None

for parent in parents:
    if parent.name == "UI":
        UI_dir = parent.name
        print('Found')

print(UI_dir)