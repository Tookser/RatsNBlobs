debug_flag = False

def debug(*text):
    if debug_flag:
        for el in text:
            print(el, ' ', end='')
        print('')

def debug_field():
    '''print all wormheads'''
    if debug_flag:
        debug('----')
        for x in range(width):
            for y in range(height):
                if field[x][y] != []:
                    #print('!')
                    if isinstance(field[x][y][0], WormHead):
                        w = field[x][y][0]
                        debug('O', x, '-', y, '-', 'o' if w._next is not None else '#',\
                        w._next, w._pred, len(w._segments), ' segments')
