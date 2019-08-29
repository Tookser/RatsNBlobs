class Vizualization():
    '''визуализация, в т.ч. анимация'''
    def __init__(self):
        self._corner = (2, 2)
        self._inventory_coord = (2, 2)
        
        self._log_last_coord = (self._corner[0] + WIDTH_OF_VIEW + 4, \
                                self._corner[1] + HEIGHT_OF_VIEW)
        self._log_first_coord = (self._log_last_coord[0], \
                                self._corner[1] + 1)
        self._NUMBER_OF_LOG_MESSAGES = self._log_last_coord[1] - self._log_first_coord[1] + 1
        
        corner_x, corner_y = self._corner
        self._HELP_POSITION = (10, 10) #позиция справки выводимой по нажатию p
        self._STATUS_BAR_POSITION = (corner_x, corner_y + HEIGHT_OF_VIEW + 2)
        self._log = log.Log()

    @property
    def log(self):
        return self._log

    def animation_decorator(function_to_decorate):
        '''декоратор для всех функций анимации'''
        def dont_animate(self, *args, **kwargs):
            pass

        return function_to_decorate if animation_flag else dont_animate


    def start_vizualize(self):
        '''визуализация начинается с вызова этого метода'''
        t.open()
        try:
            assert t.set('''window: title ='RATS''N''BLOBS 0.0.1', size={}x{};'''.\
                        format(WIDTH_OF_WINDOW, HEIGHT_OF_WINDOW))
            assert t.set('font: VeraMono.ttf, size=20')
            assert t.set('input.filter={keyboard+}')
            assert t.set("palette.light_gray = #CFCFCF");

        except:
            raise VizualizationError('can\'t set options')

    def _colors_and_symbol(self, j, i):
            '''выдаёт цвет и символ для клетки без проверки что за клетка'''
            if field_walls[j][i]:
                return (wall_color, background_color, '#')
            elif l.is_monster_in(j,i):
                monster = l.get_monster(j, i)
                return (monster.color, monster.background_color, monster.letter)
            else: #TODO отрефакторить
                obstacle = obstacles[j][i]
                if obstacle == obstacles_types.stone:
                    return (t.color_from_name(stone_color), background_color, 'o')
                elif obstacle == obstacles_types.fridge:
                    return (t.color_from_name(fridge_color), background_color, 'f')
                elif obstacle == obstacles_types.sword:
                    return (t.color_from_name(sword_color), background_color, '(')
                elif isinstance(obstacle, Item):
                    return (obstacle.color_number, background_color, obstacle.letter)
                elif obstacle != obstacles_types.space:
                    return (t.color_from_name(question_color), background_color, '?')
                else:
                    return (t.color_from_name(free_color), background_color, '.')
    
    def print_map_with_fixed_view(self, width, height):
        '''выводит карту (при фиксированном поле зрения), x, y - координаты угла'''
        x, y = self._corner
        t.print(x, y, '#' * (width + 2))
        t.print(x, y + height + 1, '#' * (width + 2))
        for i in range(height):
            t.color(t.color_from_name(wall_color))
            t.put(x, y + 1 + i, ord('#'))
            t.put(x + width + 1, y + 1 + i, ord('#'))
            for j in range(width):
                color, symbol = self._color_and_symbol(j, i)
                t.color(color)
                t.put(x + 1 + j, y + 1 + i, ord(symbol))
    
    def print_map_with_float_view(self, center_x, center_y):
        '''печать: окошко обзора перемещается с игроком и статично на экране
        center_x center_y - координаты центральной клетки'''
        corner_x, corner_y = self._corner
        t.print(corner_x, corner_y, '-' * (WIDTH_OF_VIEW + 2))
        t.print(corner_x, corner_y + HEIGHT_OF_VIEW + 1, '-' * (WIDTH_OF_VIEW + 2))
        
        assert HEIGHT_OF_VIEW == WIDTH_OF_VIEW
        
        sdvig = HEIGHT_OF_VIEW // 2
        
        #добавляется x и y (реальные координаты клетки)
        #i и j - координаты в окошке
        for i in range(HEIGHT_OF_VIEW):
            t.color(t.color_from_name(wall_color))
            t.put(corner_x, corner_y + 1 + i, ord('|'))
            t.put(corner_x + WIDTH_OF_VIEW + 1, corner_y + 1 + i, ord('|'))
            for j in range(WIDTH_OF_VIEW):
                x = j + center_x - sdvig
                y = i + center_y - sdvig 
                
                
                if x in range(l.width) and y in range(l.height):
                    #если клетка видна и существует
                    color, cell_background_color, symbol = self._colors_and_symbol(x, y)
                    
                    t.color(color)
                    t.bkcolor(cell_background_color)
                    
                    t.put(corner_x + 1 + j, corner_y + 1 + i, ord(symbol))
                else:
                    #если клетка за пределами поля, то отображается стена
                    t.color(t.color_from_name(wall_color))
                    t.bkcolor(t.color_from_name(background_color))
                    t.put(corner_x + 1 + j, corner_y + 1 + i, ord('#'))
    
    def print_log(self, x, y):
        '''печатает лог'''
        t.bkcolor(t.color_from_name(background_color))
        
        
        
        log = self.log.return_last_messages(self._NUMBER_OF_LOG_MESSAGES)
        #x, y = self._log_last_coord
        
        number_of_fresh_messages = self.log.number_of_fresh_messages
        for i in range(len(log)):
            if i < number_of_fresh_messages:
                t.color(t.color_from_name(active_log_color))
            else:
                t.color(t.color_from_name(passive_log_color))
            t.print(x, y-i, log[-i-1])
        
    
    def vizualize(self, status_bar = True):
        '''визуализирует, сначала всё стирает потом рисует
        status_bar - нужно ли показывать status bar, если он вообще включён (отключается в последней визуализации во время выигрыша/проигрыша)'''

        

        t.clear()
        t.bkcolor(t.color_from_name(background_color))
        t.color(t.color_from_name(wall_color))

        corner_x, corner_y = self._corner
        width, height = l.width, l.height

        t.print(corner_x, corner_y - 1, 'Don\'t press P to hel[color={}]p[/color].'.format(help_highlight_color))

        
        if fixed_view_flag:
            self.print_map_with_fixed_view(width, height)
        else:
            self.print_map_with_float_view(player.x, player.y)
            
            


        if side_help_flag: 
            self.side_help(corner_x + WIDTH_OF_VIEW + 3, corner_y + HEIGHT_OF_VIEW // 2)
        
        if LOG_FLAG:
            self.print_log(*self._log_last_coord)
        
        if status_bar_flag and status_bar:
            self.show_status_bar()
        #t.color(t.color_from_name(help_color))

        t.refresh()
    
    def map_mode_print_map(self, x, y):
        '''печатает карту для map_mode с центром в x, y'''
        pass
    
    def map_mode(self):
        '''пока не работает
            выводит карту для просмотра и позволяет по ней перемещаться, содержит и ввод, '''
        self.print_map_with_fixed_view(*self._corner, l.width, l.height)
        
        x, y = player.x, player.y #стартовая позиция совпадает с координатами игрока
        #key = t.read()
        
        
        while True:
            key = t.read()
            
            if key in keys_move:
                movement = keys_move[key]
                x += movement[0]
                y += movement[1]
                map_mode_move(x, y)
            if key in map_mode_stop_keys:
                break

        
        
    
    def end_vizualize(self):
        '''в конце игры закрывается окно'''
        t.close()

    def side_help(self, x, y):
        '''справка сбоку'''
        t.color(t.color_from_name(help_color))
        t.print(x, y, 'TYU')
        t.print(x, y + 1, 'G@J')
        t.print(x, y + 2, 'BNM')
        t.refresh()

    def get_color_of_health_bar(self):
        '''определяет цвет полоски здоровья'''
        
        #три цвета, переходят один в другой
        red = (130, 0, 0)
        yellow = (110, 110, 0)
        green = (0, 130, 0)
        alpha = 255
        
        def div_color(color1, color2, ratio):
            result = [round(color1[i]*ratio + color2[i]*(1-ratio)) for i in range(3)]
            #print(result)
            return result
        
        ratio = min(player.health, player.maxhealth)/player.maxhealth
        
        if ratio >= 0.6:
            result = div_color(green, yellow, (ratio-0.6)/0.4)
        else:
            result = div_color(yellow, red, (ratio/0.6))
        
        return (alpha, *result)
            
    def get_color_of_player(self):
        '''возвращает цвет игрока - как цвет полоски, но ярче'''
        result = v.get_color_of_health_bar()
        result = [min(round(x*2), 255) for x in result]
        return (result)
        
    
    def show_status_bar(self):
        '''показывает статус-бар'''
        
        x, y = self._STATUS_BAR_POSITION
        
        delta_hp_designation = 7
        delta_hp_number = 10
        delta_x_health_bar = 13 #смещение полоски здоровья
        
        
        length_of_health_bar = 22
        
        
        t.color(t.color_from_name(status_bar_color))
        t.print(x, y, 'AT:[color={}]{}[/color]'.format(attack_number_color, 
                                                    round(player.damage, 1) if player.damage < 10 
                                                                        else round(player.damage)))
        
        t.print(x + delta_hp_designation, y, 'HP:')
        t.color(t.color_from_argb(*self.get_color_of_player()))
        t.print(x + delta_hp_number, y, '{}'.format(round(player.health)))
        
        t.color(t.color_from_name(status_bar_color))
        t.put(x + delta_x_health_bar, y, '[')
        
        #t.bkcolor(t.color_from_name('green'))
        t.bkcolor(t.color_from_argb(*self.get_color_of_health_bar()))
        
        for i in range(1, 1 + \
                round(length_of_health_bar*\
                        min(player.health, player.maxhealth)/player.maxhealth)\
                ):
            t.put(x + delta_x_health_bar + i, y, ' ')
        
        t.bkcolor(t.color_from_name(background_color))        
        t.put(x + delta_x_health_bar + length_of_health_bar + 1, y, ']')
        
        
        t.bkcolor(t.color_from_name(background_color))
        t.refresh()
        
    def hide_status_bar(self):
        '''скрывает статус-бар'''
        x, y = self._STATUS_BAR_POSITION
        t.bkcolor(t.color_from_name(background_color))
        for i in range(0, WIDTH_OF_WINDOW):
            t.put(x + i, y, ' ')
        t.refresh()
    
    def show_inventory(self):
        '''показывает инвентарь, с действиями'''
        t.clear()
        x, y = self._inventory_coord
        inventory = player.inventory
        
        t.print(x, y, 'INVENTORY, [color={}]{}[/color] items'.\
                format(inventory_key_color, len(inventory)))
        
        for i in range(len(inventory)):
            t.print(x, y + i + 1, \
                '([color={}]{}[/color]) {}'.\
                format(inventory_key_color, inventory[i].letter, inventory[i].name))
        
        t.print(x, y + len(inventory) + 1, '([color={}]q[/color]) return to the game'.format(inventory_return_key_color))
        
        t.refresh()
        
        item_keys = {t.TK_A + i : i for i in range(len(inventory))}
        
        #обрабатывает инвентарь
        while True:
            key = t.read()
            if key in item_keys:
                item_number = item_keys[key] #получение номера предмета
                item = inventory[item_number].item #т.к. возвращаются namedtuple, и по .item - сам предмет
                
                if isinstance(item, Item):
                    '''если нормальный предмет'''
                    if item.auto_usable:
                        #если применяется на себя самого
                        player.use_item(item, player)
                    else:
                        #если применяется на кого-то ещё
                        
                        v.log.refresh()
                        v.log.add_message("Select the direction.")
                        v.vizualize()
                        
                        key = t.read()
                        
                        #TODO здесь обработку
                        try:
                            move = ALL_KEYS_MOVE_WITHOUT_STANDING[key]
                        except KeyError:
                            v.log.refresh()
                            v.log.add_message('Wrong direction.')
                            v.vizualize()
                            break
                        
                        target_coord = (player.x + move[0], player.y + move[1])
                        
                        if l.is_monster_in(*target_coord):
                            target = l.get_monster(*target_coord)
                            player.use_item(item, target)
                        else:
                            v.log.refresh()
                            v.log.add_message("No monster in this direction.")
                            v.vizualize()
                        
                    raise TurnCompleted
                else:
                    '''иначе просто выходим'''
                    break
            elif key == quit_from_inventory_key:
                break
            else:
                pass
    
    @animation_decorator
    def fire(self, x, y, color1='yellow', color2='white', fire_time=45, zwerg_times=7):
        '''мерцание, например, при попадании
            game field + 1
           corner->##
                   #F<-field'''
        saved_color, saved_bkcolor = t.TK_COLOR, t.TK_BKCOLOR

        x, y = x + self._corner[0] + 1, y + self._corner[1] + 1
        def put():
            t.put(x, y, symbol)
            t.refresh()
            t.delay(fire_time)

        symbol = t.pick(x, y)
        native_color = t.pick_color(x, y)
        t.color(native_color)
        native_background_color = t.pick_bkcolor(x, y)

        t.bkcolor(t.color_from_name(color1))
        put()

        def zwerg():
            t.bkcolor(t.color_from_name(color1))
            put()
            t.bkcolor(t.color_from_name(color2))
            put()

        for i in range(zwerg_times): zwerg()

        #restore


        t.color(native_color)
        #TEMPORARY HACK TODO
        t.bkcolor(t.color_from_name(background_color))
        #t.bkcolor(native_background_color)

        t.put(x, y, symbol)

        t.color(saved_color)
        t.bkcolor(saved_bkcolor)



        t.refresh()

    @animation_decorator
    def explosion(self, x, y, radius=2, form_diagonal=True, color1='yellow',\
    color2='white', fire_time=45, zwerg_times=4):
        '''explosion visualization
        form_diagonal - rotated 45* square'''
        if form_diagonal:
            saved_color, saved_bkcolor = t.TK_COLOR, t.TK_BKCOLOR
            previous_x, previous_y = x, y
            #x, y = x + self._corner[0] + 1, y + self._corner[1] + 1

            mas = range(-radius, radius + 1)
            mas2 = []
            for i in mas:
                for j in mas:
                    if abs(i) + abs(j) <= radius:
                        mas2.append((i, j))
            #print(mas2)
            #print(len(mas2))
            list_cells = [(x + i, y + j) for i, j in mas2 \
            if x + i in range(WIDTH_OF_VIEW) and (y + j) in range(HEIGHT_OF_VIEW) and \
            not field_walls[x+i][y+j]]

            list_cells = [(x + self._corner[0] + 1, y + self._corner[1] + 1) \
            for x, y in list_cells]
            '''
            for i, j in mas2:
                print ('{0}+{1} {2}+{3}'.format(x, i, y, j))
                print (x + i, y + j)
            '''
            #print(list_cells)



            def put():
                '''the main change between explosion and fire'''
                for x_here, y_here in list_cells:
                    t.color(native_colors[(x_here, y_here)])
                    t.put(x_here, y_here, symbols[(x_here, y_here)])
                t.refresh()
                t.delay(fire_time)

            symbols = {(x, y):t.pick(x, y) for x, y in list_cells}
            native_colors = {(x, y):t.pick_color(x, y) for x, y in list_cells}
            #temporary hack TODO
            #not used
            native_background_color = {(x, y):t.pick_bkcolor(x, y) for x, y in list_cells}

            def zwerg():
                t.bkcolor(t.color_from_name(color1))
                put()
                t.bkcolor(t.color_from_name(color2))
                put()

            for i in range(zwerg_times): zwerg()

            #restore

            #TEMPORARY HACK TODO
            t.bkcolor(t.color_from_name(background_color))
            #t.bkcolor(native_background_color)
            for x_here, y_here in list_cells:
                t.color(native_colors[(x_here, y_here)])
                t.put(x_here, y_here, symbols[(x_here, y_here)])

            t.color(saved_color)
            t.bkcolor(saved_bkcolor)
        else:
            raise NotImplementedError


    def help(self):
        t.clear()
        t.color(t.color_from_name(help_color))
        
        x, y = self._HELP_POSITION
        #print(t.TK_WIDTH // 2, t.TK_HEIGHT // 2 - 1, 'Press to move:')
        t.print(x, y - 1, 'Press to move:')
        t.print(x, y, 'TYU')
        t.print(x, y + 1, 'G[color={}]@[/color]J'.format(help_highlight_color))
        t.print(x, y + 2, 'BNM')
        
        t.print(x, y + 3, 'Press [color={}]H[/color] to wait.'.format(help_highlight_color))
        t.print(x, y + 4, 'Press [color={}]SPACE[/color] to pickup items'.format(help_highlight_color))

        t.refresh()
        #t.delay(3000)

    def win(self):
        v.hide_status_bar()
        v.vizualize(status_bar = False) #нужно для того, чтобы были видны сообщения произошедшие перед победой
        t.set('input.filter=keyboard') #important!

        t.color('yellow')
        #TODO чётко указать позицию выигрышной и проигрышной надписей
        t.print(v._corner[0] + WIDTH_OF_VIEW // 2 - 4, v._corner[1] + HEIGHT_OF_VIEW + 2, \
        '!YOU WIN! PRESS ANY KEY...')
        t.refresh()
        
        if PAUSE_AFTER_END_OF_GAME_FLAG:
            t.delay(PAUSE_AFTER_END_OF_GAME_LENGTH)
        key = t.read()

    def lose(self):
        v.hide_status_bar()
        v.vizualize(status_bar = False)
        
        t.set('input.filter=keyboard') #important!
        t.color('dark blue')
        t.print(v._corner[0] + WIDTH_OF_VIEW // 2 - 4, v._corner[1] + HEIGHT_OF_VIEW + 2, \
        '...You lose..... PRESS ANY KEY...')
        t.refresh()

        if PAUSE_AFTER_END_OF_GAME_FLAG:
            t.delay(PAUSE_AFTER_END_OF_GAME_LENGTH)
        key = t.read()
