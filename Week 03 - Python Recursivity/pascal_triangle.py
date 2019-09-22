from util import TriangleBuilder, caching_decorator
import pdb
import logging

logger = logging.getLogger(__name__)

class Pascal_Triangle(object):
    builder = TriangleBuilder()
    
    @caching_decorator
    def get_element_recursively(self, i, x):
        return 1 if (x == 0 or x >= i) else \
            self.get_element_recursively(i=i-1, x = x-1) + \
            self.get_element_recursively(i=i-1, x = x)
    
    def pascal_triangle_a(self, level, index=0):
        if index < level:
            row = (str(self.get_element_recursively(i=index, x=x)) for x in range(index+1))
            print(" ".join(row))
            self.pascal_triangle_a(level=level, index=index+1)
    
    def pascal_triangle_b(self, level, index=0):
        if index < level:
            row = self.builder.get_row(index=index)
            print(" ".join(row))
            self.pascal_triangle_b(level=level, index=index+1)


if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    #fire.Fire(Pascal_Triangle)
    level = 20
    temp = Pascal_Triangle()
    #pdb.set_trace()
    temp.pascal_triangle_b(level=level)
    temp.pascal_triangle_a(level=level)
    #Pascal_Triangle()
