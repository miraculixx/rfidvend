from resource import VendResource

class Customer(VendResource):
    def last_name(self):
        return self.get('last_name')