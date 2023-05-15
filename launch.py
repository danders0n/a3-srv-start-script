import os
import re
import configparser
import subprocess

from workshop import *
from configuration import *

config = configparser.ConfigParser()
config.read('server.ini')

preset = config['PATHS']['preset']

### Check OS ###
platform = ''
if os.name == 'nt':
    platform = 'Windows'
elif os.name == 'posix':
    platform = 'Linux'
# ******************************

#check_app_update()
mods_list = read_preset(preset, False)
mods_missing = check_workshop(mods_list, False)

if len(mods_missing) > 0:
    install_workshop_items(mods_missing)
#install_workshop_item('843425103')

setup_config('D:\Games\steamcmd\steamapps\common\Arma_3_Server\server.cfg')

launch = create_exec(mods_list)

print(launch)
#result = subprocess.run(launch, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)