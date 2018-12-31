'''здесь различные генераторы карт'''
import random
import os

def _close_isolated(field_walls, x_player=0, y_player=0, only_by_side=True):
    '''проверяет, какая часть поля доступна, и закрывает стенами оставшуюся
    TODO исправить flood algorithm'''
    assert not field_walls[x_player][y_player]
    
    def get_neighbours(x, y):
        '''выдаёт список соседей'''
        m = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if not only_by_side:
            m += [(1, 1), (-1, -1), (-1, 1), (1, -1)] 
        m = [(x+a, y+b) for (a, b) in m]
        return m
    
    
    width = len(field_walls)
    height = len(field_walls[0])
    print(width, height)
    avaiable_from_start_cells = [[False for j in range(height)] for i in range(width)]
    checked = [[False for j in range(height)] for i in range(width)]
    
    avaiable_from_start_cells[x_player][y_player] = True
    
    #рекурсивно проверяем, какие клетки доступны из начальной 
    def check_cell(x,y):
        if not (x in range(width) and y in range(height)):
            return

        elif checked[x][y]:
            return

        else:
            print(x, y)
            checked[x][y] = True
            avaiable_from_start_cells[x][y] = True
            
            neib = get_neighbours(x, y);
            for x_test, y_test in neib:
                if x_test in range(width) and y_test in range(height):
                    try:
                        if field_walls[x_test][y_test]:
                            checked[x_test][y_test] = True
                        else:
                            print("check", x_test, y_test)
                            check_cell(x_test, y_test)
                    except:
                        pass


    check_cell(x_player, y_player)
    
    #если клетка недоступна из начальной, то делаем её стеной
    for i in range(height):
        for j in range(width):
            if not avaiable_from_start_cells[j][i]:
                field_walls[j][i] = True

def _load_scene(file_name, width, height):
    '''загружает стены и препятствия (камни) из файла, скопировано из ratsnblobs.py'''
    def test(l):
        '''тестирует на высоту и ширину'''
        assert len(l) == height
        for sub_list in l:
            assert len(sub_list) == width

    def transp(l):
        '''транспонирует массив'''
        l = list(map(list, zip(*l))) 
        return l

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    resources_path = 'Resources'
    with open(os.path.join(resources_path, file_name + '.txt')) as f:
        '''
        ..o
        #.#
        ...
        типовая карта
        '''
        field_walls = f.readlines()
        field_walls = [s.strip() for s in field_walls]
        
        '''obstacles = [[(obstacles_types.stone if c == 'o' 
        else obstacles_types.fridge if c == 'f' 
        else obstacles_types.space) 
        for c in s] 
        for s in field_walls]'''
        field_walls = [[c == '#' for c in s] for s in field_walls]
        
        #test(obstacles)
        test(field_walls)
            
        field_walls = transp(field_walls)
        #obstacles = transp(obstacles)

        return field_walls, None #obstacles                

def _test_vizualize(field_walls, width, height):
    '''тестовая текстовая визуализация, скопирован из ratsnblobs.py'''
    def horizontal():
        for i in range(width + 2):
            print('#', end='')
        print('')
    horizontal()
    for i in range(height):
        print('#', end='')
        for j in range(width):
            #print(j, i)
            if field_walls[j][i] == False:
                print('.', end='')
            else:
                print('#', end='')
        print('#')
    horizontal()

        
def create_forest_map(x_size=20, y_size=10, cave_size=20, x_start=5, y_start=5, random_param=6):
    '''создаёт пещеру по алгоритму генерации леса отсюда http://rlgclub.ru/wiki/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F_%D0%BB%D0%B5%D1%81%D0%B0'''
    walls = [[True for i in range(y_size)] for j in range(x_size)]
    
    walls[x_start][y_start] = False 
    x_current, y_current = x_start, y_start
    
    
    
    for i in range(cave_size):
        if (random.randint(1,random_param) == 1):
            try:
                x_current += 1
                if not(x_current in range(x_size) and y_current in range(y_size)): 
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                x_current -= 1;
        if (random.randint(1,random_param) == 1):
            try:
                y_current += 1;
                if not (x_current in range(x_size) and y_current in range(y_size)):
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                y_current -= 1;
        if (random.randint(1,random_param) == 1):
            try:
                x_current += -1;
                if not (x_current in range(x_size) and y_current in range(y_size)):
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                x_current -= -1;
        if (random.randint(1,random_param) == 1):
            try:
                y_current += -1;
                if not (x_current in range(x_size) and y_current in range(y_size)):
                    raise IndexError
                walls[x_current][y_current] = False;
            except IndexError:
                y_current -= -1;
    
    return walls

def count_free(walls):
    s = 0
    for column in walls:
        for cell in column:
            s += 1 if cell == False else 0
    return s

def _test():
    print("hi!")
    
    field_walls, _ = _load_scene("test_map", 6, 5)
    _test_vizualize(field_walls, 6, 5)
    _close_isolated(field_walls, 0, 0, only_by_side = True)
    _test_vizualize(field_walls, 6, 5)
    
    s = 0
    for i in range(1000):
        walls = create_forest_map(x_size = 40, y_size = 40, cave_size = 20, x_start = 10, y_start = 10)
        s += count_free(walls)
    print (s/1000)
    _test_vizualize(walls, 40, 40)
    
if __name__ == "__main__":
    pass
    #_test()
