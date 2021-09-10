import time
import csv
import time
from w1thermsensor import W1ThermSensor

curTime=time.time()
localTime=time.localtime(curTime)

#print("The out: ", localTime)

AA=localTime.tm_year
MM=localTime.tm_mon
DD=localTime.tm_mday

HH=localTime.tm_hour
MMn=localTime.tm_min
SS=localTime.tm_sec


sensor = W1ThermSensor()

csv_file = open("Archivo_Año_mes_dia.csv", 'w')
csv_writer = csv.writer(csv_file, delimiter=",")

while True:

	tem = sensor.get_temperature()
	#print("\nHora : %d Temp : %.3f " %(HH,tem))
	curTime=time.time()
	localTime=time.localtime(curTime)
	AA=localTime.tm_year
	MM=localTime.tm_mon
	DD=localTime.tm_mday

	HH=localTime.tm_hour
	MMm=localTime.tm_min
	SS=localTime.tm_sec
	#String=str(AA)+":"+str(MM)+":"+str(DD)+" "+str(HH)+":"+str(MMm)+":"str(SS)
	String=str(AA)+str(MM)+str(DD)+" "+str(HH)+str(MMm)+str(SS)
	print(String)
	csv_writer.writerow([String,tem])
	time.sleep(10)
csv_file.close()
