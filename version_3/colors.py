class Colors:
    green = (47,230,23)
    orange = (226,116,17)
    purple = (166,0,247)
    cyan = (21,204,209)
    blue = (13,64,216)
    red = (255,0,0)       # touché
    dark_red = (128,0,0)  # coulé
    water = (0,0,50)      # eau
    miss = (100,100,100)  # tir raté, gris

    @classmethod 
    def get_cell_colors(cls):
        # index 0 = eau, 1-5 = bateaux, 11-15 = touché, 21-25 = coulé, 30 = miss
        return [
        cls.water, cls.green, cls.orange, cls.purple, cls.cyan, cls.blue,
        cls.red, cls.red, cls.red, cls.red, cls.red,
        cls.dark_red, cls.dark_red, cls.dark_red, cls.dark_red, cls.dark_red,
        cls.water, cls.water, cls.water, cls.water, cls.water,
        cls.dark_red, cls.dark_red, cls.dark_red, cls.dark_red, cls.dark_red,
        cls.water, cls.water, cls.water, cls.water,
        cls.miss
    ]
