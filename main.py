import os
import json
import re
import subprocess
import sys

directory = '/home/xmitter/.etlegacy/legacy/tvdemos/oc/tvdemos/'

out_directory = '/home/xmitter/.etlegacy/legacy/demos/nlpol/'
cut_out_directory = '/home/xmitter/.etlegacy/legacy/demos/nlpol/CUTS/'

udt_convert_path = '/home/xmitter/dev/uberdemotools/cmake-build-release/UDT_convert'
udt_cut_path = '/home/xmitter/dev/uberdemotools/cmake-build-release/UDT_cutter'


def get_players(data):
    players = {}
    for ms in data['matchStats']:
        for ps in ms['playerStats']:
            cn = ps['clientNumber']
            name = ps['cleanName']
            if ps['team'] != 'spectators':
                players[cn] = name
    return players

def get_team_players(data):
    players = get_players(data)
    team_players = {}
    for ms in data['matchStats']:
        for ps in ms['playerStats']:
            cn = ps['clientNumber']
            # name = ps['cleanName']
            team = ps['team']
            if team != 'spectators':
                team_players[team] = team_players.get(team, []) + [(cn,players[cn])]
        break # don't count after swap
    return team_players

def has_team(team_players, tag, min_count=3):
    return any((len([p for p in players if tag in p[1]]) > min_count and len([p for p in players if any(pl2.lower() in p[1].lower() for pl2 in ['w1lko', 'ght', 'meehow', 'turki', 'winq', 'jamato', 'subak'])]) < 4) for team,players in team_players.items())


def get_team(team_players, tag, min_count=3):
    for team, players in team_players.items():
        if len([p for p in players if tag in p[1]]) > min_count and len([p for p in players if any(pl2.lower() in p[1].lower() for pl2 in ['w1lko', 'ght', 'meehow', 'turki', 'winq', 'jamato', 'subak'])]) < 4:
            return players
    return []

def get_demo_path(json_path):
    return re.sub(r'\.json$', '.tv_84', json_path)

# print(get_demo_path('/home/xmitter/.etlegacy/legacy/tvdemos/oc/tvdemos/2024-10-25-174039-sw_goldrush_te.json'))


def process():
    c = 0
    dir_names = set()
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            tv_demo_path = get_demo_path(os.path.join(directory, filename))
            # print(os.path.join(directory, filename))
            with open(os.path.join(directory, filename)) as f:
                data = json.load(f)
                if 'matchStats' in data:
                    players = get_players(data)
                    tp = get_team_players(data)

                    def process_has_team(tag):
                        if has_team(tp, tag):
                            gt = get_team(tp, tag)
                            print(f"{len(gt)} {gt}")
                            for cn,name in gt:
                                dir_name = name.replace(' ','').replace('>>','').replace('NL','').replace('elysium~','').replace('NED','').lower()
                                dir_names.add(dir_name)
                                out_directory_player = os.path.join(out_directory, dir_name)
                                try:
                                    os.mkdir(out_directory_player)
                                except FileExistsError:
                                    pass

                                cp = subprocess.run([udt_convert_path, '-p=84', f"-o={out_directory_player}", f"-cn={cn}", tv_demo_path], capture_output=True)
                                print(cp.stdout.decode())
                                print(cp.stderr.decode(), file=sys.stderr)
                                # call udt_convert_path -p=84 -o={out_directory_player} -cn={cn} tv_demo_path
                                pass


                            return True
                        return False


                    if process_has_team('NL'):
                        c+=1
                    if process_has_team('>>'):
                        c += 1

    for d in dir_names:
        print(d)
    print(f'{c=}')


def check_ned():
    c = 0
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename)) as f:
                data = json.load(f)
                if 'matchStats' in data:
                    players = get_players(data)
                    # print(players)
                    for cn in players:
                        if 'NED' in players[cn]:
                            print(players[cn])


# check_ned()
# process()

def cut():
    try:
        os.mkdir(cut_out_directory)
    except FileExistsError:
        pass
    for p_dir in os.listdir(out_directory):
        # print(p_dir)
        cut_dir = os.path.join(cut_out_directory, p_dir)
        try:
            os.mkdir(cut_dir)
        except FileExistsError:
            pass
        args = [
            udt_cut_path,
            's', '-s=8', '-e=5', '-p=-1', '-duration=5', '-frags=3', '-team_kills=0', '-t=16'
            '-r', f"-o={cut_dir}",
            os.path.join(out_directory, p_dir)
        ]
        print(args)
        cp = subprocess.run(args, capture_output=True)
        print(cp.stdout.decode())
        print(cp.stderr.decode(), file=sys.stderr)

cut()