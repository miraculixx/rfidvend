#/bin/bash
echo Attach Reader to USB, press ENTER
read
stty -F /dev/ttyUSB0 speed 9600 -crtscts cs8 -cstopb -ixon raw
echo now scan any tags. it will print the serial number received
while read line
do
 echo "Scanned tag with ID=" $line 
done < /dev/ttyUSB0 
