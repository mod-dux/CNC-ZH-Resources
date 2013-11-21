import os

def remove_multiple_whitespaces(lines):
    return [' '.join(l.split())+'\n' for l in lines if l.strip()]

def remove_comment_lines(lines):
    return [l.partition(';')[0].strip()+'\n' for l in lines]

def get_lines(src):
    with open(src) as source:
        return source.readlines()

def write_lines(src, lines):
    with open(src, 'w') as destination:
        for l in lines:
            destination.write(l)

if __name__ == '__main__':
    src = os.path.join('.', 'src')
    dest = os.path.join('.', 'baked.ini')
    baked_lines = []
    for root, dir, files in os.walk(src):
        if files:
            for f in files:
                lines = get_lines(os.path.join(root, f))
                lines = remove_comment_lines(lines)
                lines = remove_multiple_whitespaces(lines)
                baked_lines.extend(lines)
    write_lines(dest, baked_lines)