from struct import unpack
import Image
import gzip

tag_types = { 0 : 'End',
			  1 : 'Byte',
			  2 : 'Short',
			  3 : 'Int',
			  4 : 'Long',
			  5 : 'Float',
			  6 : 'Double',
			  7 : 'Byte array',
			  8 : 'String',
			  9 : 'List',
			  10 : 'Compound'}

# Read number and type of list items and print them
def read_list_payload(chunk):
	list_item_type = ord(chunk.read(1))
	list_length = unpack('>l', chunk.read(4))[0]

	print "%d items of type %s" % (list_length, tag_types[list_item_type])
	
def read_byte(chunk):
	return ord(chunk.read(1))

def read_short(chunk):
	return unpack('>h', chunk.read(2))[0]
	
def read_int(chunk):
	return unpack('>l', chunk.read(4))[0]
			
def read_long(chunk):
	return unpack('>q', chunk.read(8))[0]
			
def read_byte_array(chunk):
	length = read_int(chunk)
	print "Array length: %d" % length
	payload = chunk.read(length)
	return payload
	
def read_compound(chunk):
	payload = []
	tag = read_tag(chunk)
	payload.append(tag)
	tag_type = tag[0]
	while (tag_type > 0):
		tag = read_tag(chunk)
		payload.append(tag)
		tag_type = tag[0]
	
	print "Read %d elements in compound" % len(payload)

	return payload
	
def read_string(chunk):
	str_length = unpack('>h', chunk.read(2))[0]
	if (str_length > 0):
		str = chunk.read(str_length)
		#print "Name: %s" % name
	else:
		str = None
	return str
	
# Read entire tag
def read_tag(chunk):
	type = ord(chunk.read(1)) # Chunk starts with "10" byte
	print "Found tag type: %s" % (tag_types[type], )
	if (type > 0):
		name = read_string(chunk)
		if (name != None):
			print "Name: %s" % name
	else:
		name = ''
		
	payload = None
	# Read payload of each tag. "0" tag has no payload
	if (type == 1):
		payload = read_byte(chunk)
	elif (type == 2):
		payload = read_short(chunk)
	elif (type == 3):
		payload = read_int(chunk)
	elif (type == 4):
		payload = read_long(chunk)
	elif (type == 5): # no separate float for now
		payload = read_long(chunk)
	elif (type == 6): # no separate double for now
		payload = read_long(chunk)
	elif (type == 7):
		payload = read_byte_array(chunk)
	elif (type == 8):
		payload = read_string(chunk)
	elif (type == 9):
		payload = read_list_payload(chunk)
	elif (type == 10):
		payload = read_compound(chunk)
		
	return (type, name, payload)

def getchunkname(x, y):
	def base36encode(number):
		sign = ''
		if not isinstance(number, (int, long)):
			raise TypeError('number must be an integer')
		if number < 0:
			#raise ValueError('number must be positive')
			sign = '-'
			number = number * -1

		alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

		base36 = ''
		while number:
			number, i = divmod(number, 36)
			base36 = alphabet[i] + base36

		return sign + base36 or sign + alphabet[0]

	chunk_x = -13
	chunk_y = 44
		
	filename = base36encode(divmod(chunk_x, 64)[1])  + "\\" + base36encode(divmod(chunk_y, 64)[1]) + "\\c." + base36encode(chunk_x) + "." + base36encode(chunk_y) + ".dat"

	return filename

def map_chunk_slice(x, z, y = 64):	
	map_directory = "D:\\Minemap\\!CURRENT\\dev\\shm\\rsync\\smp2\\smp\\World10\\"
		
	chunkname = map_directory + getchunkname(x, z)

	chunk = gzip.open(chunkname, 'r')

	output = read_tag(chunk)

	print output[0]

	try:
		for level in output[2]:
			# skip end tags
			if (level[0] == 0): 
				continue
				
			for tag in level[2]:
				if (tag[0] == 0):
					continue
				print tag[1]
				if tag[1] == "Blocks":
					blocks = tag[2]
					
		print "Blocks retrieved"
		print "Blocks count: %d" % len(blocks)
	except:
		print "No blocks found"
		exit(0)

	# y = 77

	# Print map by block ID
	for z in range(0, 16):
	  for x in range (0, 16):
		print ord(blocks[ y + ( z * 128 + (x * 128 * 16)) ]),
	  print 
	  
	def get_cropbox(x, y):
		return (x*16, y*16, x*16 + 16, y*16 + 16)

	terrain = Image.open("terrain.png")

	stone = terrain.crop(get_cropbox(0,0))
	dirt = terrain.crop(get_cropbox(2,0))
	grass = terrain.crop(get_cropbox(3,0))
	gravel = terrain.crop(get_cropbox(3,1))
	sand = terrain.crop(get_cropbox(2,1))
	coal = terrain.crop(get_cropbox(2,2))
	iron = terrain.crop(get_cropbox(1,2))
	gold = terrain.crop(get_cropbox(0,2))
	redstone = terrain.crop(get_cropbox(3,3))
	diamond = terrain.crop(get_cropbox(2,3))
	obsidian = terrain.crop(get_cropbox(5,2))
	bedrock = terrain.crop(get_cropbox(1,1))

	clay = terrain.crop(get_cropbox(2,0))
	log = terrain.crop(get_cropbox(5,1))
	leaves = terrain.crop(get_cropbox(4,3))
	ice = terrain.crop(get_cropbox(3,4))
	mossy_coblestone = terrain.crop(get_cropbox(4,2))

	cobblestone_block = terrain.crop(get_cropbox(0,1))
	wood_block = terrain.crop(get_cropbox(4,0))
	# bookshelf = terrain.crop(get_cropbox(4,0))
	iron_block = terrain.crop(get_cropbox(6,1))
	gold_block = terrain.crop(get_cropbox(7,1))
	diamond_block = terrain.crop(get_cropbox(8,1))
	chest = terrain.crop(get_cropbox(9,1))
	tnt = terrain.crop(get_cropbox(9,0))
	glass = terrain.crop(get_cropbox(1,3))
	soil = terrain.crop(get_cropbox(7,5))

	brick = terrain.crop(get_cropbox(7,0))
	halfblock = terrain.crop(get_cropbox(6,0))

	map = Image.new("RGB", (256, 256))

	# Draw map
	for x in range(0, 16):
	  for z in range (0, 16):
		block_id = ord(blocks[ y + ( z * 128 + (x * 128 * 16)) ])
		if block_id == 1:
			map.paste(stone, get_cropbox(x, z))
		if block_id == 2:
			map.paste(grass, get_cropbox(x, z))
		elif block_id == 3:
			map.paste(dirt, get_cropbox(x, z))
		elif block_id == 4:
			map.paste(cobblestone, get_cropbox(x, z))
		elif block_id == 5:
			map.paste(wood_block, get_cropbox(x, z))
		elif block_id == 7:
			map.paste(bedrock, get_cropbox(x, z))
		elif block_id == 12:
			map.paste(sand, get_cropbox(x, z))
		elif block_id == 13:
			map.paste(gravel, get_cropbox(x, z))
		elif block_id == 14:
			map.paste(gold, get_cropbox(x, z))
		elif block_id == 15:
			map.paste(iron, get_cropbox(x, z))
		elif block_id == 16:
			map.paste(coal, get_cropbox(x, z))
		elif block_id == 17:
			map.paste(log, get_cropbox(x, z))
		elif block_id == 18:
			map.paste(leaves, get_cropbox(x, z))
		elif block_id == 20:
			map.paste(glass, get_cropbox(x, z))
		elif block_id == 43: # both of these will look alike from above
			map.paste(halfblock, get_cropbox(x, z))
		elif block_id == 44: # both of these will look alike from above
			map.paste(halfblock, get_cropbox(x, z))
		elif block_id == 47: # Bookshelf looks like wood from above
			map.paste(wood_block, get_cropbox(x, z))
		elif block_id == 49:
			map.paste(mossy_coblestone, get_cropbox(x, z))
		elif block_id == 49:
			map.paste(obsidian, get_cropbox(x, z))
		elif block_id == 56:
			map.paste(diamond, get_cropbox(x, z))
		elif block_id == 60:
			map.paste(soil, get_cropbox(x, z))
		elif block_id == 73:
			map.paste(redstone, get_cropbox(x, z))
		elif block_id == 79:
			map.paste(ice, get_cropbox(x, z))
		elif block_id == 82:
			map.paste(clay, get_cropbox(x, z))
		
	try:
		map.save('.\map.png', 'PNG')
	except:
		print "Something went wrong on save"
		
map_chunk_slice(0,0, 78)
