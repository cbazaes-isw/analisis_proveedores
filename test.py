from datetime import datetime

class ClaseDePrueba(object):

    def getDatetime(self):
        return datetime.now()

    def __init__(self, param1):
        self.param1 = param1
        self.thisDatetime = self.getDatetime()


o = ClaseDePrueba("algun_valor")

print(o.getDatetime())
print(o.param1)
print("{o.param1} {o.thisDatetime}".format(o=o))
