class Player(Creature):
    def __init__(self, x, y, old_player=None):
        '''old_player - указатель на старого игрока, если есть и нет флага reborn_flag - здоровье копируется'''
        #super(Player, self).__init__(x, y, player_health, player_damage, player_color, '@')
        if old_player is None or reborn_flag:
            super().__init__(x, y, player_health, player_damage, player_color, \
                            '@', flag_through_rocks = True)
        else:
            super().__init__(x, y, player_health, player_damage, player_color, \
                            '@', current_health=old_player.health, flag_through_rocks = True)
        self._is_die = False
        
        self._inventory_list = [obstacles_types.stone, obstacles_types.stone]
        #self._inventory_list = []
        
        self._attack_level = 0


    def turn(self):
        '''ход игрока, в т.ч. считывание нажатий кнопок и тд'''
        #t.set('input.filter=[keyboard+]')

        v.vizualize()
        
        #t.delay(DELAY_AFTER_MOVE)
        while True:
            key = t.read()
            if t.state(help_key):
                v.help()
            elif key in [inventory_key]:
                #вызывается инвентарь и обрабатываются нажатия кнопок в нём, после него визуализация
                assert t.set('input.filter={keyboard}')
                
                try:
                    v.show_inventory() #TurnCompleted кидается, если показ инвентаря вызвал реальный ход
                except TurnCompleted:
                    assert t.set('input.filter={keyboard+}')
                    break
                    
                assert t.set('input.filter={keyboard+}')
                v.vizualize()
            else:
                v.vizualize()
            '''elif t.state(map_mode_key):
                v.map_mode()'''
            

            
            if key in keys_move:
            #if t.state(t.TK_M):
                v.log.refresh()
                movement = keys_move[key]
                self.move(self.x + movement[0], self.y + movement[1])
                break

            if NUMPAD_MOVEMENT_FLAG and key in numpad_keys_move:
                v.log.refresh()
                movement = numpad_keys_move[key]
                self.move(self.x + movement[0], self.y + movement[1])
                break

            if key in pickup_drop_key:
                v.log.refresh()
                player.pickup_item()
                '''if player.is_inventory():
                    player.drop_item()
                else:'''
                    
                    
            if key == t.TK_CLOSE:
                game.end_game_please()
                v.end_vizualize()
                break
            '''is_movement = False
            for key in keys_move:
                if t.state(key):
                    movement = keys_move[key]
                    self.move(self.x + movement[0], self.y + movement[1])
                    is_movement = True
                    break
            if is_movement:
                break'''

        #t.set('input.filter=[]')
        
        #v.vizualize() #TODO может, убрать, не порушит ли анимацию
        
        
        t.delay(after_delay if is_delay else 0)

        
    def use_item(self, item, target):
        '''применяет предмет, TODO сделать повторно используемые'''
        item.use(target)
        self._inventory_list.remove(item)
        

    @property
    def inventory(self):
        '''возвращает инвентарь в виде списка namedtuple'''
        def get_name(item):
            '''возвращает имя, под которым объект входит в инвентарь'''
            d = {obstacles_types.stone: 'stone',
                    obstacles_types.sword: 'sword'}
            if isinstance(item, Item):
                return item.name
            else:
                return d[item]

        Item_in_inventory = collections.namedtuple('Item_in_inventory', ['name', 'letter', 'item'])
        
        result = []
        for i in range(len(self._inventory_list)):
            item = self._inventory_list[i]
            result.append(Item_in_inventory(get_name(item), chr(ord('a')+i), item))
        return result
        
    def is_can_pickup(self, item):
        '''проверка, можно ли взять предмет в инвентарь'''
        return len(self._inventory_list) < SIZE_OF_INVENTORY
    
    def pickup_item(self):
        '''поднять предмет, если не может - пропуск хода'''
        item = obstacles[self.x][self.y]
        
        if (item in list_of_pickupable_obstacles or \
                    isinstance(item, Item)) and \
                    self.is_can_pickup(item):
            self._inventory_list.append(item)
            if item is obstacles_types.sword:
                self._attack_level += 1
            obstacles[self.x][self.y] = obstacles_types.space
        else:
            pass


    def _die(self):
        '''умереть. ставит флаг'''
        super()._die()
        self._is_die = True

    def is_die(self):
        return self._is_die
    
    @property
    def damage(self):
        '''у игрока урон зависит от уровня атаки'''
        return self._attack_level*2 + self._damage
    
    @property
    def attack_level(self):
        return self._attack_level
    
    @property
    def color(self):
        return t.color_from_argb(*v.get_color_of_player())
