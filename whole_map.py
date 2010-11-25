import os
import Image
import read_chunk

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

whole_map = Image.new("RGB", (image_width * 4 + 1, image_height * 4 + 1))

print "Image size: %d by %d" % (image_width, image_height)
cur_chunk = 0

for chunk in chunks:
	#if (chunk[0] > min_x) & (chunk[0] < max_x) & (chunk[1] > min_z) & (chunk[1] > max_z):
	#print chunk
	try:
		chunk_image = read_chunk.map_chunk_slice(chunk[0], chunk[1], 70);
		
		chunk_image = chunk_image.resize((4,4), Image.ANTIALIAS)
	except:
		chunk_image = Image.new("RGB", (4,4))
	#whole_map.putpixel((chunk[0] - min_x, chunk[1] - min_z), (111,175,75))
	whole_map.paste(chunk_image, ((chunk[0] - min_x) * 4, (chunk[0] - min_z) * 4, (chunk[0] - min_x) * 4 + 4, (chunk[0] - min_z) * 4 + 4))
	cur_chunk = cur_chunk + 1
	if (cur_chunk % 100) == 0:
		print "%f percent done" % (cur_chunk * 100 / num_chunks)
	
# whole_map = whole_map.resize((image_width * 4, image_height * 4), Image.ANTIALIAS)

whole_map.save('whole_map.png')