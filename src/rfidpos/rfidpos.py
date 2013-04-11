from vendhq.api import *

class RFIDPos:
    def __init__(self, url, user, password):
        self.vendurl = url
        self.vendpassword = password
        self.venduser = user
        self.cus_by_rfid = {}
        self.init_vend()
        self.init_cus_cache()
        
    def init_vend(self):
        self.vend = Vend(url=self.vendurl)
        self.vend.connect(user=self.venduser, password=self.vendpassword)
        self.registers = self.vend.get_registers()
        self.taxes = self.vend.get_taxes()
        self.products = self.vend.get_products()
        self.payment_types = self.vend.get_payment_types()

    def init_cus_cache(self):
        self.customers = self.vend.get_customers()
        for cus in self.customers:
            self.cus_by_rfid[cus.get('custom_field_1')] = cus

    def create_sale(self, register=None, customer=None, product=None, payment_type=None, tax=None):
        sproduct = Product()
        sproduct.set('product_id', product.get('id'))
        sproduct.set('quantity', 1)
        sproduct.set('price', 50.50)
        sproduct.set('tax', 0.0)
        sproduct.set('tax_id', tax.get('id'))
        sproduct.set('tax_total', 0.0)

        sale = Sale();
        sale.set('register_id', register.get('id'))
        sale.set('customer_id', customer.get('id'))
        sale.set('user_name', self.venduser)
        sale.set('total_price', 50.50)
        sale.set('total_tax', 0)
        sale.set('tax_name', tax.get('name'))
        sale.set('status', 'SAVED')
        sale.set('note', None)
        sale.add_product(sproduct)

        payment = Payment()
        payment.set('retailer_payment_type_id', payment_type.get('id'))
        payment.set('amount', 50.50)
        sale.add_payment(payment)
        print "Filled sale: >%s<" % sale
        return sale

    def create_sale_from_tag(self, tag=None):
        # find customer for this tag
        if tag.get_id() in self.cus_by_rfid:
            tagcus = self.cus_by_rfid[tag.get_id()]
        else:
            return None
        # create the sale
        sale = self.create_sale(register=self.registers[0],
                                customer=tagcus,
                                product=self.products[0],
                                tax=self.taxes[0],
                                payment_type=self.payment_types[0])
        # post and finalize the sale
        new_sale = self.vend.post('register_sales', sale)
        return new_sale
