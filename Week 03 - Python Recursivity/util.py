def print_name():
    print(__name__)

def _corner_case_decorator(func):
    def wrap(self, i, j, *args, **kwargs):
        if j >= i or j == 0:
            return 1
        return func(self, i=i, j=j, *args, **kwargs)
    return wrap


def caching_decorator(func):
    CACHE = {}
    
    def wrapper(self, **kwargs): # arguments that can be used as dictionaries
        key = hash(frozenset(kwargs.items())) # key that represent the kwargs from the function
        if key in CACHE:
            return CACHE[key]
        CACHE[key] = func(self, **kwargs)
        return CACHE[key]
        
    return wrapper

class TriangleBuilder(object):
    CACHE = {}
    
    def save(self, i, j, value):
        self.CACHE[(i, j)] = lambda: value
        return value
    
    @_corner_case_decorator
    def get(self, i, j, default=lambda: None):
        #if j >= i or j == 0:   #conditions not needed anymore, because the decorator
        #    return 1
        return self.CACHE.get((i, j), default)() # this las parentesis is to
                                                 # get the value of the lambda function
    
    @_corner_case_decorator
    def create(self, i, j):
        #if j >= i or j == 0:
        #    return 1
        upper_left = self.get_or_create(i=i-1, j=j-1)
        upper_center = self.get_or_create(i=i-1, j=j)
        return self.save(i=i, j=j, value= upper_center+upper_left)
    
    def get_or_create(self, i, j):
        return self.get(i, j, default=lambda: self.create(i,j))
    
    def get_row(self, index):
        return [str(self.get_or_create(index, j)) for j in range(index+1)]
    
