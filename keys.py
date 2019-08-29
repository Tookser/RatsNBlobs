import bearlibterminal.terminal as t

keys_move = {t.TK_T:(-1, -1),
        t.TK_Y:(0, -1),
        t.TK_U:(1, -1),
        t.TK_G:(-1, 0),
        t.TK_H:(0, 0),
        t.TK_J:(1, 0),
        t.TK_B:(-1, 1),
        t.TK_N:(0, 1),
        t.TK_M:(1, 1)
        }

numpad_keys_move = {t.TK_KP_7:(-1, -1),
    t.TK_KP_8:(0, -1),
    t.TK_KP_9:(1, -1),
    t.TK_KP_4:(-1, 0),
    t.TK_KP_5:(0, 0),
    t.TK_KP_6:(1, 0),
    t.TK_KP_1:(-1, 1),
    t.TK_KP_2:(0, 1),
    t.TK_KP_3:(1, 1)
    }

help_key = t.TK_P
inventory_key = t.TK_I
quit_from_inventory_key = t.TK_Q


map_mode_key = t.TK_SHIFT
        
pickup_drop_key = [t.TK_SPACE]

map_mode_stop_keys = [t.TK_SHIFT]