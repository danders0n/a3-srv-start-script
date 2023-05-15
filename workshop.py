import os
import re
import configparser
import subprocess

config = configparser.ConfigParser()
config.read('server.ini')

def module_separator():
    print('\n------------------------------\n')

# *** check check if needed mods are up to date or installed ***
def check_workshop(mods_preset, print_mods):
    # TODO: Make it work with steamcmd
    #       Steamcmd after start dosen't know where mods are,
    #       you need to download one mod to get dir path.
    #       Download smallest mods possible then check for updates
    #       and redownload outdated items...
    #       CBA_A3 download will be safest 450814997
    print('Check_Workshop: Checking for workshop items...')
    mods_directory = config['PATHS']['workshop']
    mods_installed = os.listdir(mods_directory)
    mods_ids = []
    mods_missing = []

    for mod in mods_preset:
        if mod[1] in mods_installed:
            if print_mods:
                print('Check_Workshop: ' + mod[0] + ' is installed!')
        else:
            if print_mods:
                print('Check_Workshop: ' + mod[0] + ' is missing!')
            mods_missing.append(mod[1])

    if len(mods_missing) == 0:
        print('Check_Workshop: All required mods are installed!')
    if len(mods_missing) == 1 :
        print('Check_Workshop: ' + str(len(mods_missing)) + ' mod needs to be installed!')
    if len(mods_missing) > 1 :
        print('Check_Workshop: ' + str(len(mods_missing)) + ' mods needs to be installed!')
    module_separator()
    return mods_missing
# ******************************

# *** try to install mod from steam workshop ***
def install_workshop_item(mod_id):
    print('Install_Workshop_Item: Installing ' + mod_id + '...')
    steamcmd = config['PATHS']['steamcmd_exec']
    credentials = config['PATHS']['login']
    command = steamcmd + ' +login ' + credentials +' +workshop_download_item 107410 ' + mod_id +' validate +quit'
    result = subprocess.run(command, capture_output=True, text=True)
    #print(str(result))
    for i in range (0, 4):
        if re.search('Success', str(result)):
            status = 'Install_Workshop_Item: '+ mod_id + ' successfully downloaded!'
            return_val = True
            break
        elif re.search('ERROR! Timeout', str(result)):
            status = 'Install_Workshop_Item: '+ mod_id + ' Timeout, retrying! Try left: ' + str((4-i))
            result = subprocess.run(command, capture_output=True, text=True)
        else:
            status = 'Install_Workshop_Item: Something went wrong with: ' + mod_id
            return_val = False
            break

    print(status)
    return return_val
# ******************************

# *** loop over missing mods ***
def install_workshop_items(mods_list):
    if len(mods_list) == 1:
        print('Install_Workshop_Item: Installing ' + str(len(mods_list)) + ' missing mod from preset...')
    elif len(mods_list) > 1:
        print('Install_Workshop_Item: Installing ' + str(len(mods_list)) + ' missing mods from preset...')
    for mod in mods_list:
        install_workshop_item(mod)

    module_separator()
# ******************************