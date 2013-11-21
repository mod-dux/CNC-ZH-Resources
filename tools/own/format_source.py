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
            indent = indent + 1
        for k in ['Object ', 'ConditionState', 'DefaultConditionState', 'ArmorSet',
                  'WeaponSet', 'UnitSpecificSounds', 'TransitionState', 'Prerequisites',
                  'AttackAreaDecal', 'TargetingReticleDecal', 'DeliveryDecal\n',
                  'Turret\n', 'ObjectReskin ', 'GridDecalTemplate']:
            if active_line.startswith(k) and not (active_line.startswith('Object ') and ignore_object):
                indent = indent + 1
        if 'Prerequisites' in active_line:
            ignore_object = True
    return l

def get_lines(src):
    with open(src) as source:
        return source.readlines()

def write_lines(src, lines):
    with open(src, 'w') as destination:
        for l in lines:
            destination.write(l)

if __name__ == '__main__':
    src = os.path.join('.', 'src')
    for root, dir, files in os.walk(src):
        if files:
            for f in files:
                lines = get_lines(os.path.join(root, f))
                lines = clear_indentation(lines)
                lines = reindent_lines(lines)
                write_lines(os.path.join(root, f), lines)