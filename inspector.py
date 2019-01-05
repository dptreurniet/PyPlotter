class Inspector:
    def __init__(self):
        self.objects = {}

    def add(self, reference, object):
        if reference in self.objects.keys():
            raise IndexError('Reference already in use')
        self.objects[reference] = object

    def remove(self, reference):
        del self.objects[reference]

    def get(self, reference):
        try:
            return self.objects[reference]
        except Exception as e:
            print('Error: %s' % e)
