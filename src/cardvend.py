from vendhq.api import *
from datetime import datetime

import webbrowser
import config

def test_get_customers():
  print json.dumps(vend.get('customers'), indent=2)
  print json.dumps(vend.get('customers', { "code": "JDO"}), indent=2)

  customers = vend.get_customers()
  print "Found %d customers" % len(customers)
  for cus in customers:
      print cus.last_name()

def test_get_registers():
  registers = vend.get_registers()
  for reg in registers:
    print reg.get('id')
    print reg.get('name')

def test_get_sales():
    sales = vend.get_sales()
    print "%d sales found" % len(sales)
    for sale in sales:
     print "Register: %s Amount: %d" % (sale.get('register_id'), sale.get('total_price'))
     print sale

def test_get_products():
  products = vend.get_products()
  print "%d products found" % len(products)
  for product in products:
    print product

def test_get_payment_types():
  types = vend.get_payment_types()
  print "%d payment types found:" % len(types)
  for type in types:
      print type

def test_get_taxes():
  taxes = vend.get_taxes()
  print "%d taxes found:" % len(taxes)
  for tax in taxes:
      print tax

def test_post_sales():
  registers = vend.get_registers()
  taxes = vend.get_taxes()
  customers = vend.get_customers()
  products = vend.get_products()

  product = Product()
  product.set('product_id', products[0].get('id'))
  product.set('quantity', 1)
  product.set('price', 50.50)
  product.set('tax', 0.0)
  product.set('tax_id', taxes[0].get('id'))
  product.set('tax_total', 0.0)

  sale = Sale();
  sale.set('register_id', registers[0].get('id'))
  sale.set('customer_id', customers[0].get('id'))
  sale.set('user_name', 'ps@novapp.ch')
  sale.set('total_price', 50.50)
  sale.set('total_tax', 0)
  sale.set('tax_name', taxes[0].get('name'))
  sale.set('status', 'SAVED')
  sale.set('note', None)
  sale.add_product(product)

  types = vend.get_payment_types()

  payment = Payment()
  payment.set('retailer_payment_type_id', types[0].get('id'))
  payment.set('amount', 50.50)
  sale.add_payment(payment)

  print "Filled sale: >%s<" % sale

  #vend.url = "http://localhost/"
  new_sale = vend.post('register_sales', sale)
  print new_sale

  webbrowser.open(vend.gen_url_sale(new_sale))

config = config.rfidpos_config

vend = Vend(config['VENDHQ_URL'])
vend.connect(user=config['VENDHQ_USER'], password=config['VENDHQ_PASS'])

#test_get_payment_types()
#test_get_taxes()
test_post_sales()
exit()
