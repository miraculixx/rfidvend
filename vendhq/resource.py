import json

class VendResource:
    def __init__(self, data=None):
        if not data == None:
            self.data = data
        else:
            self.data = {}
        #print "init vend resource data: %s" % self

    def get(self, attribute, default=""):
        if attribute in self.data:
            return self.data[attribute]
        else:
            return default

    def set(self, attribute, value):
        self.data[attribute] = value

    def __str__(self):
        return json.dumps(self.data, indent=2)

    def __dict__(self):
        return self.data