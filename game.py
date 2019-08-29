@singleton.singleton
class Game():
    '''Класс игры, содержащий по идее всё: игровое поле, очередь, игрока, класс визуализации...'''
    def __init__(self):
        self._game_closed = False
        self._is_first_level = True

    def cycle(self):
        '''основной цикл игры, ходы игрока и смерть'''
        while True:
            #print(irq.ammount, ' ', player.health)
            creature = irq.get()
            creature.turn()
            creature.do_effects_after_turn()
            
            if l.end_of_game():
                if not player.is_die():
                    v.win()
                    break
                elif player.is_die():
                    v.lose()
                    break
                else:
                    pass

                '''elif game.is_next_level(): ??'''


    def new_level(self, lg, l, field, field_walls, obstacles, irq, h, player=None):
        '''update vars'''
        self.lg = lg
        self.l = l
        self.field = field
        self.field_walls = field_walls
        self.obstacles = obstacles
        self.irq = irq
        self.h = h
        #if player is not None:
        self.player = player
    
        if self._is_first_level:
            self._is_first_level = False
            v.log.add_message("Game begins.")
        else:
            v.log.add_message("Next level.")
    
    def end_game_please(self):
        self._game_closed = True
        
    @property
    def is_game_closed(self):
        return self._game_closed
