import sys
import subprocess
import os
import pkg_resources

cur_file_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', '--user'])

def installl(namee):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', namee])
def updatee(namee):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', namee, '--upgrade'])

installed_packages = pkg_resources.working_set
installed_packages_list = sorted([f'{i.key}' for i in installed_packages])
for i in installed_packages_list:
    if 'kivy' in i:
        place = installed_packages_list.index(i)
        installed_packages_list[place] = ''

with open(f'{cur_file_path}/requirements.txt', 'r') as filee:
    data = filee.readlines()
    for i in data:
        place = data.index(i)
        data[place] = i.replace('\n','')

    for packg in data:
        if packg not in installed_packages_list:
            installl(packg)
for i in range(len(installed_packages_list)):
    if installed_packages_list[i] != '':
        updatee(installed_packages_list[i])


