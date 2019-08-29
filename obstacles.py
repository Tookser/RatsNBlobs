import collections 

#возможные препятствия, новые - добавлять в конец, чтобы не сбилась нумерация
list_of_obstacles = ['space', 'wall', 'stone', 'fridge', 'sword']
tuple_of_type_of_obstacles = collections.namedtuple('type_of_obstacles', ' '.join(list_of_obstacles))
#сами константы препятствий, использовать их
obstacles_types = tuple_of_type_of_obstacles(*range(len(list_of_obstacles)))

list_of_pickupable_obstacles = [obstacles_types.stone, obstacles_types.sword]