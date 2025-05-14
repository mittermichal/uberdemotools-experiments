import os

def_directory = '/home/michal/et/legacy/demos/2025-kimi-3s'  # directory of demos to be played
demo_directory = '/home/michal/et/legacy/demos'  # where game looks up demos


def process(directory, demos):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if filename.endswith(".dm_84"):
            demos.append(os.path.relpath(path, demo_directory))
        if os.path.isdir(path):
            process(path, demos)


demos = []
process(def_directory, demos)
# f = open(os.path.join(demo_directory, '/../demo_play.cfg'), 'w')
f = open('demo_play_spring3s.cfg', 'w')
"""
set _demo1 "demo 2024-10-14-185849-etl_adlernest; set nextdemo vstr _demo2"
"""
for idx, demo in enumerate(demos):
    if idx>300:
        break
    out = f'set _d{idx} "demo {demos[idx][:-6]}; set nextdemo vstr _d{idx + 1}"'
    print(out)
    f.write(out + '\n')
out = f'vstr _d0\n'
print(out)
f.write(out)
f.close()
