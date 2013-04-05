import urllib2
import base64
import json

from customer import Customer
from register import Register
from sale import Sale
from product import Product
from payment import Payment
from payment_type import PaymentType
from tax import Tax

class Vend:
  def __init__(self, url=""):
      self.url = url
      
  def connect(self, user="", password=""):
    self.user = user
    self.password = password

  def request(self, api, data=None):
    request = urllib2.Request("%s/api/%s" % (self.url, api), data)
    base64string = base64.encodestring('%s:%s' % (self.user, self.password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    return request

  def get(self, resource, param=[]):
     # prepare parameter string, if any
     if len(param) > 0:
       params = ""
       for key in param:
         params = "%s/%s" % (key, param[key])
       api = '%s/%s' % (resource, params)
     else:
        api = resource
     # get an authorized Request
     request = self.request(api)
     print request.get_full_url()
     # get and return result
     result = urllib2.urlopen(request)
     return json.loads(result.read())

  def get_customers(self, param=[]):
     list = self.get('customers', param)
     customers = []
     if 'customers' in list:
        for cur in list['customers']:
            customers.append(Customer(data=cur))
     return customers

  def get_registers(self, param=[]):
      list = self.get('registers', param)
      registers = []
      if 'registers' in list:
          for cur in list['registers']:
              registers.append(Register(data=cur))
      return registers

  def get_sales(self, param=[]):
      list = self.get('register_sales', param)
      sales = []
      if 'register_sales' in list:
          for cur in list['register_sales']:
              sales.append(Sale(data=cur))
      return sales

  def get_products(self):
      list = self.get('products')
      sales = []
      if 'products' in list:
          for cur in list['products']:
              sales.append(Sale(data=cur))
      return sales

  def get_payment_types(self):
      list = self.get('payment_types')
      types = []
      if 'payment_types' in list:
          for cur in list['payment_types']:
              types.append(PaymentType(data=cur))
      return types

  def get_taxes(self):
      list = self.get('taxes')
      taxes = []
      if 'taxes' in list:
          for cur in list['taxes']:
              taxes.append(Tax(data=cur))
      return taxes

  def gen_url_sale(self, sale):
      url = "%s/sell#sale/%s" % (self.url, sale.get('id'))
      print url
      return url
  
  def post(self, resource, obj):
     request = self.request(resource, obj.__str__())
     result = urllib2.urlopen(request)
     list = json.loads(result.read())
     if resource == "register_sales":
         if 'register_sale' in list:
             return Sale(data=list['register_sale'])
     return list
