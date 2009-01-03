import cerealizer as c

class A(object):
    def __init__(self, lol):
        self.lol = lol


a=A({'hihii':'ok'})
c.register(A)
b = c.dumps(a)
print b

d = c.loads(b)
print d, d.lol
