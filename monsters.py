'''
Классы монстров.
Включается только "include"-ом
'''


class Rat(Creature):
    '''blind rat:)'''
    def __init__(self, x, y):
        #super(Rat, self).__init__(x, y, rat_health, rat_damage, \
        #['red', 'darkest gray', 'darker gray', 'gray'], 'r')
        super().__init__(x, y, 3, 1, ['red', 'darkest gray', 'darker gray', 'gray'], 'r')

    def turn(self):
        if abs(player.x - self.x) <= 1 and abs(player.y - self.y) <= 1:
            self.move(player.x, player.y)
        else:
            dx, dy = random.choice(neighbour_cells)
            self.move(self.x + dx, self.y + dy)

class RatS(Rat):
    def turn(self):
        '''work only if player exists
        copypasted from wiki'''
        x1, y1 = self.x, self.y
        x2, y2 = player.x, player.y

        dx = x2 - x1
        dy = y2 - y1

        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

        if dx < 0: dx = -dx
        if dy < 0: dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = x1, y1

        error, t = el/2, 0


        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        self.move(x, y)

class Blob(Creature):
    def __init__(self, x, y):
        #super(Blob, self).__init__(x, y, 1, 0, ['red', 'lime'], 'b')
        super().__init__(x, y, 1, 0, ['red', 'lime'], 'b')
        self._blowdamage = 2
        self._condition = 0 #number of step

    def turn(self):
        steps = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.move(self.x + steps[self._condition][0], self.y + steps[self._condition][1])
        self._condition = (self._condition + 1) % 4


    def _die(self):
        v.explosion(self._x, self._y)
        super()._die()

        area = [(-2, 0), (-1, 0), (1, 0), (2, 0), (0, 2), (0, 1), (0, -1), (0, -2), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        assert len(area) == 12

        for e in area:
            x, y = self.x + e[0], self.y + e[1]
            if x in range(width) and y in range(height):
                if l.is_monster_in(x, y):
                    field[x][y][0].suffer(self._blowdamage)


class Creeper(Creature):
    '''creates blob behind itself'''
    def __init__(self, x, y):
        super().__init__(x, y, 10, 0.0, \
        ['red', 'red', 'red', 'dark yellow', 'dark yellow', \
        'yellow', 'yellow', 'light blue', 'light blue', 'lighter blue', 'lighter blue']\
        , 'C')

    def turn(self):
        '''random move'''
        cells = [(self.x + i, self.y + j) for i, j in neighbour_cells if l.is_free(self.x + i, self.y + j)]
        #print(all([is_free(*c) for c in cells]))
        cell = random.choice(cells) if cells != [] else None

        if cell is not None:
            #print(is_free(*cell))
            old_cell = (self.x, self.y)
            self.move(*cell)
            if l.is_free(*old_cell):
                Blob(*old_cell)
            else:
                raise MoveError('Creeper can\'t create new creature', old_cell, l.is_free(*old_cell), cell, l.is_free(*cell))

class WormHead(Creature):
    def __init__(self, x, y, list_of_segments, health=4):
        '''list of segments, from head to tail
        put after all'''
        assert isinstance(list_of_segments, list)
        super().__init__(x, y, health, 0.34,\
        #['red']*5 + ['darkest green']*6 + ['darker green']*10 + ['green']*10 + ['light green'] * 10, 'O')
        ['red', 'yellow', 'yellow', 'green', 'green'], 'O')
        #['red']*41, 'O')

        self._segments = list_of_segments

        for el in list_of_segments:
            el.head = self

        self._next = self._pred = None
        self._stadia = 0
        self._direction = random.randint(0, 3)

        self._segments = [self] + self._segments
        for i, element in enumerate(self._segments[1:]):
            if not isinstance(element, WormSegment):
                raise WormError('not segment in list of segments, number {}'.format(str(i)))
            if not((abs(element.x-self._segments[i].x) == 1 or \
            abs(element.y-self._segments[i].y) == 1) and \
            abs(element.x-self._segments[i].x)*abs(element.y-self._segments[i].y) == 0):
                debug('t')
                raise WormError('Error in list of segments of Worm')



        if len(self._segments) >= 2:
            self._next = self._segments[1]
        self._segments = self.__class__.link(self._segments)

        self._segments = self._segments[1:]

    @staticmethod
    def link(list_of_segments):
        assert isinstance(list_of_segments, list)
        if len(list_of_segments) >= 2:
            #print ('>2')
            #print('input of function')
            #print(list_of_segments)
            for i, el in enumerate(list_of_segments[1:-1]):
                #print('o')
                #print('oy ', i + 1)
                #print('ssilka na ', i, ' ', i+2)
                el._next = list_of_segments[i+2]
                el._pred = list_of_segments[i]

                #list_of_segments[i]._next = list_of_segments[i+2]._pred = el
            list_of_segments[-1]._next = list_of_segments[0]._pred = None
            list_of_segments[0]._next = list_of_segments[1]
            list_of_segments[-1]._pred = list_of_segments[-2]
            #print('result of function')
            #print(list_of_segments)
        elif len(list_of_segments) == 1:
            list_of_segments[0]._next = list_of_segments[0]._pred = None
        else:
            raise WormError('0 elements in list_of_segments + head')

        return list_of_segments

    def move(self, x, y):
        if l.is_free(x, y):
            xn, yn = x, y
            x, y = self.x, self.y
            super().move(xn, yn)
            if len(self._segments) > 0:
                #x, y = self.x, self.y
                for el in self._segments:
                    xn, yn = el.x, el.y
                    el.move(x, y)
                    x, y = xn, yn
        elif l.get_monster(x, y) not in self._segments:
            self.attack(x, y)

    def turn(self):
        '''spontaneously change direction'''
        #to move
        d = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        d = [(self.x + i, self.y + j) for i, j in d]

        #to attack
        n = [(self.x + i, self.y + j) for i, j in neighbour_cells]

        if random.random() < 0.2 \
        or not l.is_free(d[self._direction][0], d[self._direction][1]):
            self._direction = (self._direction + random.choice([-1, 1])) % 4

        if abs(player.x-self.x) <= 1 and abs(player.y-self.y) <= 1 and random.random() < 0.9:
            self.attack(player.x, player.y)
        else:
            self.move(d[self._direction][0], d[self._direction][1])

        '''
        #square
        stadies = [(0, 1)]*4 + [(1,0)]*4 + [(0, -1)]*4 + [(-1, 0)]*4
        xa, ya = stadies[self._stadia][0], stadies[self._stadia][1]

        self.move(self.x + xa, self.y + ya)
        self._stadia = (self._stadia + 1) % len(stadies)'''

    def _die(self):
        super()._die()
        if self._next is not None:
            neck = self._next._next
            x, y = self._next.x, self._next.y
            health = self._next.health
            self._next.force_death()

            segments = self._segments[1:]

            w = WormHead(x, y, segments, health)
            if neck is not None:
                neck._pred = w

    def delete_segments_from(self, el):
        position = self._segments.index(el)
        self._segments = self._segments[:position]

    @staticmethod
    def create_worm(mas):
        '''создаёт червя по угловым точкам'''
        assert isinstance(mas, list)
        assert len(mas) >= 1
        for el in mas:
            assert len(el) == 2
        for i, el in enumerate(mas[:-1]):
            assert el[0] == mas[i+1][0] or el[1] == mas[i+1][1]
            assert not (el[0] == mas[i+1][0] and el[1] == mas[i+1][1])
            assert mas[i] != mas[i+1]

        def line(a, b):
            ''' [a, b)'''
            assert isinstance(a, list)
            assert isinstance(b, list)
            assert len(a) == len(b) == 2
            small_list = []

            if a[0] == b[0]:
                if a[1] < b[1]:
                    for i in range(0, b[1] - a[1]):
                        small_list.append([a[0], a[1] + i])
                else:
                    for i in range(0, a[1] - b[1]):
                        small_list.append([a[0], a[1] - i])
                    #small_list = list(reversed(small_list))
            else:
                if a[0] < b[0]:
                    for i in range(0, b[0] - a[0]):
                        small_list.append([a[0] + i, a[1]])
                else:
                    for i in range(0, a[0] - b[0]):
                        small_list.append([a[0] - i, a[1]])
                    #small_list = list(reversed(small_list))

            return small_list

        list_of_cells = []

        #debug(line([1, 2], [1, 10]))
        #debug(line([1, 4], [1, 0]))
        #debug(line([4, 3], [10, 3]))
        #debug(line([8, 2], [3, 2]))

        #a, b
        for i in range(len(mas) - 1):
            list_of_cells += line(mas[i], mas[i + 1])
        list_of_cells.append(mas[-1])

        x_head, y_head = list_of_cells[0][0], list_of_cells[0][1]
        list_of_cells = list_of_cells[1:]


        debug(list_of_cells)

        segments = []
        for el in list_of_cells:
            segments.append(WormSegment(*el))
        debug(x_head, y_head)
        debug(list_of_cells)
        WormHead(x_head, y_head, segments)

        return list_of_cells


class WormSegment(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, 4, 0.34,\
        #['red']*41, 'o')
        #['red']*5 + ['darkest green']*6 + ['darker green']*10 + ['green']*10 + ['light green'] * 10, 'o')
        ['red', 'yellow', 'yellow', 'green', 'green'], 'o')
        self._pred = self._next = None

    def turn(self):
        pass

    def move(self, x, y):
        if l.is_free(x, y):
            super().move(x, y)

    def _die(self):
        super()._die()
        #delete from head
        if self.head is not None:
            #print('delete segments')
            self.head.delete_segments_from(self)

        if self._next is not None:
            #print('y')
            neck = self._next._next
            x, y, health = self._next.x, self._next.y, self._next.health

            self._next.force_death()

            #get list of segments of 2 (H111d222)
            segments = []
            t = neck
            while t != None:
                segments.append(t)
                t = t._next
            #print('none? ', l)
            w = WormHead(x, y, segments, health)
            if neck is not None:
                neck._pred = w

        if self._pred is not None:
            #print('delete next u pred')
            self._pred._next = None

        #raise NotImplementedError

    def force_death(self):
        super()._die()

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, h):
        self._head = h
