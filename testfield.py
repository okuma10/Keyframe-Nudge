from pathlib import Path



parents = Path(__file__).parents
root_dir = Path(__file__).parent
# for parent in parents:
#     print(f'{parent.name}')
#     if parent.name == "BlenderDrawDev":
#         root_dir = str(parent)
print(Path(__file__).parent)
print(type(root_dir))

log_file = str(root_dir) + '\\UI\\Shaders\\shader.log'

# print(log_file)

path = Path('C:\\Users\\Okuma_10\\AppData\\Roaming\\Blender Foundation\\Blender\\2.82\\scripts\\addons\\Keyframe-Nudge-master\\UI\\Fonts\\123.txt')
print(path.exists())
with open(path, 'r') as file:
    print(file.read())
