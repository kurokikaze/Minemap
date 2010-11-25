import os
import Image

map_directory = "D:\\Minemap\\!CURRENT\\dev\\shm\\rsync\\smp2\\smp\\World10\\"

num_chunks = 0

min_x = 0
max_x = 0
min_z = 0
max_z = 0

first_level = os.listdir(map_directory)

chunks = []

for file in first_level:
	if (os.path.isdir(os.path.join(map_directory, file)) & (file != 'players')):
		# print "Dir: %s" % file
		second_level = os.listdir(os.path.join(map_directory, file))
		for file_second in second_level:
			#print 'File: %s' % chunk_file
			if os.path.isdir(os.path.join(os.path.join(map_directory, file), file_second)):
				third_level = os.listdir(os.path.join(map_directory, file, file_second))
				for chunk_file in third_level:
					if(chunk_file[0:2] == 'c.'): # Just in case
						chunk_coords = chunk_file[2:-4].partition('.')
						# print chunk_coords
						if (chunk_coords[0] != '') & (chunk_coords[2] != ''):
							chunk_x = int(chunk_coords[0], 36)
							chunk_z = int(chunk_coords[2], 36)
							
							if chunk_x < min_x:
								min_x = chunk_x
							if chunk_x > max_x:
								max_x = chunk_x
							if chunk_z < min_z:
								min_z = chunk_z
							if chunk_z > max_z:
								max_z = chunk_z
							
							num_chunks += 1
							
							chunks.append((chunk_x, chunk_z))
					
print "Chunks found: %d" % num_chunks
print
print "# Map coordinates"
print
print "X is from %d to %d" % (min_x, max_x)
print "Z is from %d to %d" % (min_z, max_z)

image_width = max_x - min_x
image_height = max_z - min_z

whole_map = Image.new("RGB", (image_width, image_height))

print "Image size: %d by %d" % (image_width, image_height)

for chunk in chunks:
	#if (chunk[0] > min_x) & (chunk[0] < max_x) & (chunk[1] > min_z) & (chunk[1] > max_z):
	#print chunk
	whole_map.putpixel((chunk[0] - min_x, chunk[1] - min_z), (111,175,75))
	
whole_map.save('whole_map.png')