import os
import re
import configparser
import subprocess

config = configparser.ConfigParser()
config.read('server.ini')

def module_separator():
    print('\n------------------------------\n')

# *** read html preset ***
def read_preset(preset, print_mods):
    print('Read_Preset: Loading mods list...')
    with open(preset) as file:
        mods = [[]]
        i = 0
        while line := file.readline():
            modName =re.search('DisplayName">(.*)</td>', line)
            modId = re.search('id=(.*)" ', line)
            if modName:
                mods[i].append(modName.group(1))
                mods.append([])  
            if modId:
                mods[i].append(modId.group(1))
                i= i + 1        
            modName = modId = ""
        mods_list = [i for i in mods if i]

        print('Read_Preset: Found ' + str(len(mods_list)) + ' mods!')

        i = 0
        if print_mods:
            for mod_arr in mods_list:
                i += 1
                if i < 10:
                    print('Read_Preset: 0' + str(i) + ': ' + mod_arr[0])
                else:
                    print('Read_Preset: ' + str(i) + ': ' + mod_arr[0])
        module_separator()
    return mods_list
# ******************************

# *** check for server updates ***
def check_app_update():
    print('App_Update_Check: Checking for app updates...\n')
    steamcmd = config['PATHS']['steamcmd_exec']

    command = steamcmd + ' +login ' + credentials +' +app_update 233780 validate +quit'
    result = subprocess.run(command, capture_output=True, text=True)

    #print(str(result))
    if re.search('Success! App \'233780\' fully installed.', str(result)):
        status = 'App_Update_Check: Server is up to date!'
    else: 
        status = 'App_Update_Check: Something went wrong!'

    print(status)
    module_separator()
    return status
# ******************************

# get exec and config file
# set settings 
# copy mission to mpmission
# save settings
config_template = [
    ['hostname', '"Fun and Test Server"'],
    ['password', '""'],
    ['passwordAdmin', '"xyz"'],
    ['serverCommandPassword', '"xyzxyz"'],
    ['logFile', '"server_console.log"'],
    ['admins[]', '{"76561198054972867"}'],
    ['motd[]', '{"", "", "Welcome to our server", "We are looking for tacticool - Join us Now!", ""}'],
    ['motdInterval', '5'],
    ['maxPlayers', '64'],
    ['kickDuplicate', '1'],
    ['verifySignatures', '2'],
    ['equalModRequired', '0'],
    ['allowedFilePatching', '0'],
    ['filePatchingExceptions[]', '{""}'],
    ['voteMissionPlayers', '1'],
    ['voteThreshold', '0.33'],
    ['disableVoN', '1'],
    ['vonCodec', '1'],
    ['vonCodecQuality', '30'],
    ['persistent', '0'],
    ['timeStampFormat', '"short"'],
    ['BattlEye', '1'],
    ['allowedLoadFileExtensions[]', '{"b64","hpp","sqs","sqf","fsm","cpp","paa","txt","xml","inc","ext","sqm","ods","fxy","lip","csv","kb","bik","bikb","html","htm","biedi"}'],
    ['allowedPreprocessFileExtensions[]', '{"b64","hpp","sqs","sqf","fsm","cpp","paa","txt","xml","inc","ext","sqm","ods","fxy","lip","csv","kb","bik","bikb","html","htm","biedi"}'],
    ['allowedHTMLLoadExtensions[]', '{"htm","html","xml","txt"}'],
    ['disconnectTimeout', '5'],
    ['maxDesync', '150'],
    ['maxPing', '250'],
    ['maxPacketLoss', '50'],
    ['kickClientsOnSlowNetwork[]', '{0, 0, 0, 0 }'],
    ['kickTimeout[]', '{ {0, -1}, {1, 180}, {2, 180}, {3, 180} }'],
    ['votingTimeOut[]', '{60, 90}'],
    ['roleTimeOut[]', '{90, 120}'],
    ['briefingTimeOut[]', '{60, 90}'],
    ['debriefingTimeOut[]', '{45, 60}'],
    ['lobbyIdleTimeout', '300'],
    ['onUserConnected', '""'],
    ['onUserDisconnected', '""'],
    ['doubleIdDetected', '""'],
    ['onUnsignedData', '"kick (_this select 0)"'],
    ['onHackedData', '"kick (_this select 0)"'],
    ['onDifferentData', '""'],
    ['randomMissionOrder', 'false'],
    ['autoSelectMission', 'true'],
    ['class Missions', '{}'],
    ['missionWhitelist[]', '{}']
]

def setup_mission():
    mission_file = config['MISSION']['file']
    mission_file = mission_file.replace('.pbo', '')
    difficulty = config['MISSION']['difficulty']
    #print(line)
    for param in config_template:
        #print(param[0])
        if param[0] == 'class Missions':
            line = '\n{\n\ttemplate = ' + mission_file + ';\n\tdificulty = "' + difficulty + '";\n\tclass Params {};\n}'
            param[1] = line
    
def setup_config(config_file):
    server = list(config.items('SERVER'))
    setup_mission()
    for param in config_template:
        #print(param[1])
        for i in server:
            if param[0].lower() in i[0].lower():
                if param[0] == 'hostname':
                    param[1] = '"' + config['MISSION']['name'] + ' - ' + i[1] + '"'
                elif param[0] == 'password':
                    param[1] = '"' + i[1] + '"'
                else:
                    param[1] = '"' + i[1] + '"'
    
    with open (config_file, "w") as file:
        for param in config_template:
            #print(param)
            if param[0] == "class Missions":
                line = param[0] + param[1] + ';\n'
            else:
                line = param[0] + ' = ' + param[1] + ';\n'

            file.write(line)
    file.close()

#setup_config('D:\Games\steamcmd\steamapps\common\Arma_3_Server\server.cfg')

def copy_keys(mod_path):
    # TODO: copy keys, validate keys?
    #       what to do if keys not found? 
    #       need mod name
    #       some mods don't need keys e.g. ace compact
    keys = mod_path + '\keys'
    if os.path.exists(keys):
        print (mod_path + ' keys found!')
    else:
        print (mod_path + ' keys not found!')

def create_exec(mods_list):
    #create mod string
    mods = ['-mod="']
    path = config['PATHS']['workshop']

    for mod in mods_list:
        line = path + '\\' + mod[1]
        copy_keys(line)
        line = line + ';'
        mods.append(line)

    mods_joined = ''.join(mods)
    mods_joined = mods_joined[:-1]
    mods_joined = mods_joined + '"'
    launch = [
            config['PATHS']['server_exec'],
            '-name=server',
            '-port=2302',
            '-config=server.cfg',
            '-world=empty',
            '-filePatching',
            mods_joined
        ]
    return launch