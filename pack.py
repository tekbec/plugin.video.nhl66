import os.path, shutil, xmltodict


FILES = [
    'addon.py',
    'addon.xml',
    'service.py'
]
FOLDERS = [
    'resources'
]


addon_xml = None
with open('addon.xml') as file:
    addon_xml = xmltodict.parse(file.read())
version = addon_xml['addon']['@version']

dir_path = os.path.dirname(os.path.realpath(__file__))
zip_path = os.path.join(dir_path, '_zip')
content_path = os.path.join(zip_path, 'content')
addon_id = os.path.basename(dir_path)
addon_path = os.path.join(content_path, addon_id)
zip_file = os.path.join(zip_path, f'{addon_id}-{version}.zip')

print(f'Starting {addon_id}-{version} packaging...')

print('Removing existing files...')
if os.path.isdir(zip_path):
    shutil.rmtree(zip_path)

print('Creating directories...')
os.mkdir(zip_path)
os.mkdir(content_path)
os.mkdir(addon_path)

print('Copying files...')
for file in FILES:
    shutil.copyfile(file, os.path.join(addon_path, file))

print('Copying folders...')
for folder in FOLDERS:
    shutil.copytree(folder, os.path.join(addon_path, folder), ignore=shutil.ignore_patterns('*.pyc'))

print('Removing empty folders...')
for path, _, _ in list(os.walk(addon_path)):
    if len(os.listdir(path)) == 0:
        os.rmdir(path)

print('Zipping...')
shutil.make_archive(zip_file[:-4], 'zip', content_path)