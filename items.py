class Poison(Item):
    '''пузырёк с ядом'''
    def __init__(self, x, y, poison_length = 20, poison_damage = 2.):
        super().__init__(x, y, name = "Poison", auto_usable = False, letter = '!', color_number = t.color_from_name('green'))
        self._poison_length = poison_length
        self._poison_damage = poison_damage
    
    def use(self, target):
        '''отравляет цель, если стоит вплотную'''
        if abs(player.x - target.x) <= 1 and\
            abs(player.y - target.y) <= 1:
            target.receive_poison(self._poison_length, self._poison_damage)
        else:
            raise UseError
