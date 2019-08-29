class InfiniteRandomQueue:
    '''очередь монстров, которые должны двигаться.
    В ней содержатся все монстры по разу,
    когда исчерпывается - создаём заново, в рандомном порядке
    move from RtL, then throw LtR'''
    def __init__(self):
        self._left = []
        self._right = []
        self._ammount = 0
        self._rammount = 0
        self._lammount = 0
        self._turn_number = 0

    def append(self, item):
        '''add element'''
        self._right.append(item)
        random.shuffle(self._right)
        self._ammount += 1
        self._rammount += 1


    def get(self):
        '''выдаёт элемент из очереди
        get element from InfiniteRandomQueue'''
        if self._right == []:
            if self._left == []:
                raise IRQueueError('There is no items')
            self._right = self._left
            random.shuffle(self._right)
            self._left = []
            self._rammount, self._lammount = self._lammount, self._rammount
            self._turn_number += 1
            h.run_daemons()
        result = self._right[-1]
        self._left.append(result)
        del self._right[-1]

        self._rammount -= 1
        self._lammount += 1
        return result

    def delete(self, creature):
        '''удаляет существо из очереди (нужно при смерти, например) 
        TODO чуть рефакторнуть'''
        try:
            self._right.remove(creature)
            self._rammount -= 1
            self._ammount -= 1
        except ValueError:
            try:
                self._left.remove(creature)
                self._lammount -= 1
                self._ammount -= 1
            except ValueError:
                raise IRQueueError('Can\'t delete from queue, there is no such creature')


    @property
    def ammount(self):
        return self._ammount

    @property
    def turn_number(self):
        return self._turn_number
