
CPU_TYPE_ARM = 12
CPU_SUBTYPE_ARM_V7 = 9


def get_int(handle):
	return int(handle.read(4).encode('hex'), 16)

def checkARMv7(filePath):
	handle = open(filePath, "rb")
	handle.seek(0)
	fat_magic = get_int(handle)
	if(fat_magic != 0xcafebabe):
		handle.close()
		return False

	machoCount = get_int(handle)
	for i in range(0, machoCount):
		cpu_type = get_int(handle)
		cpu_subtype = get_int(handle)
		offset = get_int(handle)
		size = get_int(handle)
		align = get_int(handle)

		if(cpu_type == CPU_TYPE_ARM and cpu_subtype == CPU_SUBTYPE_ARM_V7):
			handle.close()
			return True
			#print("cpu_type: %d, cpu_subtype: %d, offset: %d, size: %d, align: %d\n" % (cpu_type, cpu_subtype, offset, size, align))

	handle.close()
	return False

def extractARMv7(filePath, fileDestination):
	handle = open(filePath, "rb")
	handle.seek(0)
	fat_magic = get_int(handle)
	if(fat_magic != 0xcafebabe):
		handle.close()
		return False

	machoCount = get_int(handle)
	for i in range(0, machoCount):
		cpu_type = get_int(handle)
		cpu_subtype = get_int(handle)
		offset = get_int(handle)
		size = get_int(handle)
		align = get_int(handle)

		if(cpu_type == CPU_TYPE_ARM and cpu_subtype == CPU_SUBTYPE_ARM_V7):
			handle.seek(offset)
			out = handle.read(size)
			output = open(fileDestination, "w")
			output.write(out)
			output.close()
			handle.close()
			return True
			#print("cpu_type: %d, cpu_subtype: %d, offset: %d, size: %d, align: %d\n" % (cpu_type, cpu_subtype, offset, size, align))

	handle.close()
	return False