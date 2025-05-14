#!/usr/bin/python3

import sys
import subprocess
import os
import json
import re

"""
in: paths to tvdemo stats json
out: paths to converted demos
"""


def get_players(data):
    players = {}
    for ms in data['matchStats']:
        for ps in ms['playerStats']:
            cn = ps['clientNumber']
            name = ps['cleanName']
            if ps['team'] != 'spectators':
                players[cn] = name
    return players


def get_demo_path(json_path):
    return re.sub(r'\.json$', '.tv_84', json_path)

def sanitize_filename(filename: str) -> str:
    forbidden_chars = r'\W'
    return re.sub(forbidden_chars, '_', filename, re.ASCII)

def process_stats_json(path):
    print(path)
    with open(path) as f:
        data = json.load(f)
        players = get_players(data)
        for cn, player in players.items():
            #out_dir_path = os.path.join(os.path.dirname(path),'dm_84', player).replace(' ', '_')
            out_base_dir_path = re.sub(r'\.json$','', path) 
            out_dir_path = os.path.join(out_base_dir_path, f"{sanitize_filename(player)}-{cn}")
            try:
                os.mkdir(out_base_dir_path)
            except FileExistsError:
                pass
            try:
                os.mkdir(out_dir_path)
            except FileExistsError:
                pass
            args = ['/home/michal/dev/uberdemotools/cmake-build-relwithdebinfo/udt_converter', '-t=4', '-p=84', f"-o={out_dir_path}", f"-cn={cn}", get_demo_path(path)]
            print(args)
            cp = subprocess.run(args, capture_output=True)
            print(cp.stdout.decode())
            print(cp.stderr.decode(), file=sys.stderr)



input_paths = sys.argv[1:]
for input_path in input_paths:
    process_stats_json(input_path)
