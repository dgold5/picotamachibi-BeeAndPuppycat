""" Responsible for loading values saved to the save.txt file for restoring game state"""
tracked_vars = ['that_legal_tender', 'health', 'happiness', 'energy', 'inventory']
for item in tracked_vars:
    locals()[item] = None

try:
    with open('save.txt') as f:
        for line in f:
            if line.isspace():
                pass
            elif line.startswith('inventory'):
                inventory = line.split(',')[1:]
            else:
                (key, val) = line.split()
                locals()[key] = val

except OSError:
    print('Failed to open save.txt')

def save_game():
    with open('save.txt', 'w') as f:
        for item in tracked_vars:
            if item == 'inventory':
                f.write(str(item) + ',' + ','.join(locals()[item]))
                #print(str(item) + ',' + ','.join(locals()[item]))
            else:
                f.write(str(item) + ' ' + str(locals()[item])+'\n')
                #print(str(item) + ' ' + str(locals()[item])+'\n')
    