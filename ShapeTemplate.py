class ShapeTemplate():
    def __init__(self):
        self.I_TEMP = [['..o..',
                        '..o..',
                        '..o..',
                        '..o..',
                        '.....'],
    
                        ['.....',
                        '.....',
                        'oooo.',
                        '.....',
                        '.....']]

        self.L_TEMP = [['.....',
                        '..o..',
                        '..o..',
                        '..oo.',
                        '.....'],
        
                        ['.....',
                        '.....',
                        '.ooo.',
                        '.o...',
                        '.....'],
        
                        ['.....',
                        '.oo..',
                        '..o..',
                        '..o..',
                        '.....'],
        
                        ['.....',
                        '...o.',
                        '.ooo.',
                        '.....',
                        '.....']]

        self.J_TEMP = [['.....',
                        '..o..',
                        '..o..',
                        '.oo..',
                        '.....'],
        
                        ['.....',
                        '.o...',
                        '.ooo.',
                        '.....',
                        '.....'],
        
                        ['.....',
                        '..oo.',
                        '..o..',
                        '..o..',
                        '.....'],
        
                        ['.....',
                         '.....',
                         '.ooo.',
                         '...o.',
                         '.....']]

        self.S_TEMP = [['.....',
                        '.....',
                        '..oo.',
                        '.oo..',
                        '.....'],

                        ['.....',
                        '.o...',
                        '.oo..',
                        '..o..',
                        '.....']]

        self.Z_TEMP = [['.....',
                        '.....',
                        '.oo..',
                        '..oo.',
                        '.....'],
        
                        ['.....',
                        '...o.',
                        '..oo.',
                        '..o..',
                        '.....']]

        self.T_TEMP = [['.....',
                        '..o..',
                        '.ooo.',
                        '.....',
                        '.....'],
        
                        ['.....',
                        '..o..',
                        '..oo.',
                        '..o..',
                        '.....'],
        
                        ['.....',
                        '.....',
                        '.ooo.',
                        '..o..',
                        '.....'],
        
                        ['.....',
                        '..o..',
                        '.oo..',
                        '..o..',
                        '.....']]

        self.O_TEMP = [['.....',
                        '.....',
                        '..oo.',
                        '..oo.',
                        '.....']]

    def get_shape(self, shape_name):
        if shape_name == 'I':
            return self.I_TEMP
        elif shape_name == 'L':
            return self.L_TEMP
        elif shape_name == 'J':
            return self.J_TEMP
        elif shape_name == 'S':
            return self.S_TEMP
        elif shape_name == 'Z':
            return self.Z_TEMP
        elif shape_name == 'T':
            return self.T_TEMP
        elif shape_name == 'O':
            return self.O_TEMP