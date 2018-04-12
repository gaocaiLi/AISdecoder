import gzip
import sys
import ais
import os
import time

decoded_observations = 0
all_observations = 0

def decode(filename):

	file  = gzip.open(filename, 'r')
	output = open("decoded.txt", "a")

	global decoded_observations
	global all_observations
	timestamp = '0'

	for line in file:
		all_observations = all_observations +1
		try:
			line_list = line.split(",")
			field_0 = line_list[0]

			if(field_0[0] != "!"):
				# timestamp is present
				timestamp = field_0[:17]
			field_6 = line_list[6].rstrip('\r\n')

			if (str(field_6)[0] == "0"):
				decoded = str((ais.decode(str(line_list[5]), 0)))
				## insert current timestamp value
				timestamp_position = (decoded).find("timestamp") + 12
				decoded_timestamp = decoded[:timestamp_position] + str(timestamp) + decoded[timestamp_position+3:]
	 			output.write(decoded_timestamp+ '\n\n')
				decoded_observations = decoded_observations +1
			else:
				file.readline()      # skip next line as it is a part of previous observation
		except Exception: 
			pass
	print ("Successfully decoded observations: " + str(decoded_observations) +"/" + str(all_observations) + " (" + str(float(decoded_observations)/float(all_observations)) + ")")	


start = time.time()
for filename in os.listdir(os.getcwd()):
	if filename.endswith(".txt.gz"):
		print ("decoding " + filename)
		decode(filename)
		continue
	else:
		continue

end = time.time()
print("Time elapsed: " + str(end - start))
print("The data has been decoded and stored in decoded.txt")
