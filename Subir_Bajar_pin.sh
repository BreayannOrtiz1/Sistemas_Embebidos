#!/bin/bash
#echo "17" > /sys/class/gpio/export
sleep 1
#echo "out" > /sys/class/gpio/gpio17/direction
sleep 1

for((;;))
do
 echo "1" > /sys/class/gpio/gpio17/value
 echo "0" > /sys/class/gpio/gpio17/value
 #sleep 1
done
