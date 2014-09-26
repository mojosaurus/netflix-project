__author__ = 'mojosaurus'
# No setter, only getter. This will be used as a decorator
def constant(f):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)
