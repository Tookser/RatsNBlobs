
class Item:
    def __init__(self, x, y, name = "Unknown item", auto_usable = True, \
                letter = '?', color_number = t.color_from_argb(100, 100, 100, 100)):
        if l.is_free(x, y):
            obstacles[x][y] = self
        else:
            raise MoveError('something under the {} in {}:{}'.format(self.__class__.__name__, x, y))
        
        self._auto_usable = auto_usable
        self._name = name
        self._letter = letter
        self._color_number = color_number
    
    @property
    def name(self):
        return self._name
        
    @property
    def letter(self):
        return self._letter

    @property
    def color_number(self):
        return self._color_number
        
    @property
    def auto_usable(self):
        '''применим ли предмет только на самого себя'''
        return self._auto_usable
        
    @abc.abstractmethod
    def use(self, target):
        '''применение на цель, target - цель'''
        raise NotImplementedError

