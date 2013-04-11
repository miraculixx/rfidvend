from resource import VendResource

class Sale(VendResource):
    pass

    def add_product(self, product):
        if not 'register_sale_products' in self.data:
            self.data['register_sale_products'] = []
        products = self.data['register_sale_products']
        sale_product = {}
        for k in product.data:
            sale_product[k] = product.data[k]
        products.append(sale_product)

    def add_payment(self, payment):
        if not 'register_sale_payments' in self.data:
            self.data['register_sale_payments'] = []
        payments = self.data['register_sale_payments']
        sale_payment = {}
        for k in payment.data:
            sale_payment[k] = payment.data[k]
        payments.append(sale_payment)
            