import ShapeTemplate
from ShapeTemplate import *

class Shapes():
    def __init__(self):
        self.shapes = {'I': (ShapeTemplate().get_shape('I'), '0'),
                       'L': (ShapeTemplate().get_shape('L'), '1'),
                       'J': (ShapeTemplate().get_shape('J'), '2'),
                       'S': (ShapeTemplate().get_shape('S'), '3'),
                       'Z': (ShapeTemplate().get_shape('Z'), '4'),
                       'T': (ShapeTemplate().get_shape('T'), '5'),
                       'O': (ShapeTemplate().get_shape('O'), '6')}

    def get_shapes(self):
        return self.shapes