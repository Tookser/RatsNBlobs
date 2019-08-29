class SpawnQueue(list):
    '''очередь периодических событий'''
    def __init__(self):
        super(SpawnQueue, self).__init__()
    
    def run_daemons(self):
        '''запускает демонов данного хода'''
        if self != []:
            while self[0][0] == irq.turn_number:
                #получаем событие, и вызываем функцию к аргументам
                turn_number, daemon_function, arguments = self.pop()
                daemon_function(*arguments)
    
    def _monster_spawn(self, x, y, type_of_monster, interval=10, infinite_repeat = True):
        '''spawn, который создаёт монстра через interval, 
            если infinite_repeat - он повторяется через соответствующее время до бесконечности'''
        add_monster(x, y, type_of_monster)
        if infinite_repeat:
            heapq.heappush(self, \
                            (\
                            irq.turn_number + interval, \
                            self._monster_spawn, #при этом self остаётся параметром\ метода
                            (x, y, type_of_monster, interval, infinite_repeat) \
                            ) \
                        )
    
    def add_monster_spawn(self, x, y, type_of_monster, interval=10, infinite_repeat = True):
        '''добавляет "периодическое событие" _monster_spawn через interval ходов
        если infinite_repeat - то будет повторяться до бесконечности'''
        heapq.heappush(\
            self, \
            (irq.turn_number + interval, \
            self._monster_spawn, \
            (x, y, type_of_monster, interval, infinite_repeat)\
            ))