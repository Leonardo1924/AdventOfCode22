
def process_input(filename):
    """Acquire input data"""
    
    with open(filename) as file:
        input = file.read().splitlines()
    
    input.append('$ EOF')

    return input

def process_commands(commands):
    filesystem = []
    cur_dir = -1
    directory = ''
    inode = -1
    for l, command_line in enumerate(commands):
        # print(l, command_line)
        token = command_line.split()
        if token[0] == '$':
            if directory != '':
                inode += 1
                filesystem.append(directory)
                cur_dir = inode
                directory = ''
            command = token[1]
            if command == 'cd':
                argument = token[2]
                if argument == '..':
                    cur_dir = filesystem[cur_dir]['parent']
                    dir_name = filesystem[cur_dir]['dir_name']
                else:
                    parent_dir = cur_dir
                    dir_name = argument
            elif command == 'ls':
                directory = {'dir_name':dir_name,'parent':parent_dir, 'files':[], 'dirs':[], 'total_size':0}
        elif token[0] == 'dir':
            subdir = token[1]
            directory['dirs'].append(subdir)
        else:
            size = int(token[0])
            file = token[1]
            directory['files'].append((file,size))
            directory['total_size'] += size
            # percolate file size up the tree
            pdir = directory['parent']
            while True:
                if pdir == -1: break
                filesystem[pdir]['total_size'] += size
                pdir = filesystem[pdir]['parent']

    return filesystem

#-----------------------------------------------------------------------------------------

filename = 'day7/input.txt'
#filename = 'sample.txt'

commands = process_input(filename)

filesystem = process_commands(commands)

directory_sum = 0

total_disk_space = 70000000
used_space = filesystem[0]['total_size']
unused_space = total_disk_space - used_space

required_unused  = 30000000
space_to_free = required_unused - unused_space

best_delete_size = total_disk_space
delete_dir = ''

for directory_inode, directory in enumerate(filesystem):
    dir_size = directory['total_size']
    if dir_size <= 100000:
        directory_sum += dir_size
    if dir_size >= space_to_free:
        if dir_size < best_delete_size:
            best_delete_size = dir_size
            delete_dir = directory['dir_name']

print('')
print('Part 1 answer:', directory_sum)
print('Part 2 answer: delete dir',delete_dir,'to free',best_delete_size)
print('')
