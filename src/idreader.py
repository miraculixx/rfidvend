import rfid
import time
import urllib2

reader = rfid.RFIDReader()

'''
start = time.time()
create_sale_from_tag(rfid.RFIDTag("450052C606D7"))
stop = time.time()
print "Creating a sale from tag took %d sec" % (stop - start)
'''

rfidpos_url = "http://localhost:5000"
rfidpos_url = "http://novapp.eu01.aws.af.cm/"

# read from RFID reader, if a tag detected attempt to
# create a sale automatically
while True:
    tag = reader.read()
    print "Id = %s" % tag
    start = time.time()
    request = urllib2.Request("%s/cardtrx?cardid=%s" % (rfidpos_url, tag))
    response = urllib2.urlopen(request)
    print response.read()
    stop = time.time()
    print "Creating a sale from tag ID=%s took %d sec" % (tag, stop - start)
