class CellHolder(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, x, y):
        #if not field_walls[x][y]:
        if l.is_free(x, y):
            field[x][y].append(self)
        else:
            raise MoveError('something under the {} in {}:{}'.format(self.__class__.__name__, x, y))
        self._x = x
        self._y = y
