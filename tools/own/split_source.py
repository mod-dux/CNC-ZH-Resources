import os

any_in = lambda a, b: any(i in b for i in a)

def clear_indentation(lines):
    return [l.strip()+'\n' for l in lines]

def reindent_lines(lines):
    l = []
    indent = 0
    ignore_object = False
    for line in lines:
        active_line = line.partition(';')[0]
        active_line = active_line.replace('END', 'End')
        if active_line.startswith('End ') or active_line.startswith('End\n') or active_line.endswith('End'):
            indent = indent - 1
            ignore_object = False
        nl = '  ' * indent + line
        l.append(nl.rstrip()+'\n')
        if any_in(['ModuleTag', 'SpyTag', 'Behavior', 'DrawTag', 'BodyTag'], active_line):
            if not 'UpgradeToRemove' in active_line:
                indent = indent + 1
        for k in ['Object ', 'ConditionState', 'DefaultConditionState', 'ArmorSet',
                  'WeaponSet', 'UnitSpecificSounds', 'TransitionState', 'Prerequisites',
                  'AttackAreaDecal', 'TargetingReticleDecal', 'DeliveryDecal\n',
                  'Turret\n', 'AltTurret\n', 'ObjectReskin ', 'GridDecalTemplate', 'UnitSpecificFX']:
            if active_line.startswith(k) and not (active_line.startswith('Object ') and ignore_object):
                indent = indent + 1
        if 'Prerequisites' in active_line:
            ignore_object = True
    return l

def split_files(lines):
    active = False
    filename = ''
    file_lines = []
    files = {}
    for line in lines:
        if line.startswith('Object'):
            filename = line.split(' ')[1].strip()
            print(filename)
            active = True
            file_lines = []
        if active:
            file_lines.append(line)
        if line.startswith('End'):
            active = False
            files[filename] = file_lines
    return files

def get_lines(src):
    with open(src) as source:
        return source.readlines()

def write_lines(src, lines):
    with open(src, 'w') as destination:
        for l in lines:
            destination.write(l)

if __name__ == '__main__':
    src = os.path.join('.', 'src', 'Data', 'INI', 'Object')
    directory = os.path.join('.', 'src', 'split')
    if not os.path.exists(directory):
        os.makedirs(directory)
    for root, dir, files in os.walk(src):
        if files:
            for f in files:
                directory = os.path.join('.', 'src', 'split', f)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                lines = get_lines(os.path.join(root, f))
                lines = clear_indentation(lines)
                lines = reindent_lines(lines)
                new_files = split_files(lines)
                for filename in new_files:
                    with open(os.path.join(directory, '{filename}.ini'.format(filename=filename)), 'w') as destination:
                        for l in new_files[filename]:
                            destination.write(l)
