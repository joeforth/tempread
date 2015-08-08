import serial
import time
import numpy as np
import matplotlib.pyplot as pp
m = 100
pp.ion()
pp.show()
filename = raw_input('Enter file name -->')
filename = filename + '.csv'

ser = serial.Serial('/dev/ttyS0',9600,7,'O',stopbits=1,timeout=2)
timelist = []
minlist = []
temp = []
plottemp = []
plottime = []
t0 = time.time()
#Set it up to take 12 hours of data, one reading every minute
t = 0 #Counter
n = 900 #Number of readings
delta_t = 60 #Time between readings in seconds

while t < n:
	time_init = time.time()
	ser.write("CRDG?\r\n") #Read temperature in degrees Celsius
	x = ser.read(50) #Read 50 bytes of output. Do not reduce this number.
	x = x[1:7]
	temp.append(x)
	#Plotting section
	plottemp.append(float(x))
	plottime.append(time_init - t0)
	pp.scatter(plottime,plottemp)
	pp.xlabel('Time (s)')
	pp.ylabel('Temperature (deg C)')
	pp.draw()
	#Time section
	timestring = str(time_init - t0)
	mindiff = str((time_init - t0)/60) #Time stamp in minutes
	minlist.append(mindiff)
	timelist.append(timestring) #Write time stamp
	t = t + 1
	timecorr = (t + 1) * delta_t #The amount of time at which next reading should begin
	timepassed = time.time() - t0 #Calculate time taken to take reading
	time.sleep(timecorr - timepassed) #Wait until required time gap has passed
	#Clear plot window	
	pp.cla()
def MakeFile(filename):
	"""
		MakeFile(file_name): makes a file.
	"""

	temp_path = '/home/joe/pyTemp/' + filename
	file = open(temp_path, 'w')
	file.write('')
	file.close()
	print 'File written'

MakeFile(filename)
f = open('/home/joe/pyTemp/' + filename, 'w')

# Write data file, 1st column is time in seconds, 2nd column is time in minutes, 3rd column is temperature in Celsius
i = 0
for i in range(n-1):
	f.write(timelist[i])
	f.write('\t')
	f.write(minlist[i])
	f.write('\t')
	f.write(temp[i])
	f.write('\n')

f.close()

