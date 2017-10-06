from idc import *
from idaapi import *
from idautils import *
import os
import hashlib
import re

def main():
	autoWait()

	#first_ea = MinEA()

	inDir = get_input_file_path()
	inDir = inDir.replace(get_root_filename(), "")

	text_file = open(inDir + "Output.txt", "a")


	#text_file.write("[DEBUG] Starting to hash file %s\n" % (get_root_filename()))

	for first_ea in Segments():
		for funcea in Functions(SegStart(first_ea), SegEnd(first_ea)):
			funcLen = 0
			functionName = GetFunctionName(funcea)
			funcType = GetType(funcea)

			if(funcType is None):
				continue

			#print("[DEBUG] Moving to function %s" % (hex(funcea)))
			concat = ""
			for (startea, endea) in Chunks(funcea):
				for head in Heads(startea, endea):
					opnum = op_count(head)
					name = GetMnem(head)
					for i in range(0, opnum):
						optype, val = op(head, i)
						if(optype == 1):
							name = name + " R,"
						else:
							name = name + " ADDR,"

					funcLen = funcLen + 1
					concat = concat + name

			if(funcLen <= 20):
				continue

			m = hashlib.md5()
			m.update(concat)
			my_hash = m.hexdigest()
			#print("[DEBUG] Created hash %s for function %s\n" % (my_hash, hex(funcea)))
			text_file.write("%s, %s, %s, %d\n" % (my_hash, functionName, hex(funcea), funcLen))
			
	text_file.close()
	idc.Exit(0)
					
		
def op_count(ea):
	'''Return the number of operands of given instruction'''
	length = idaapi.decode_insn(ea)
	for c,v in enumerate(idaapi.cmd.Operands):
		if v.type == idaapi.o_void:
			return c
		continue
	# maximum operand count. ida might be wrong here...
	return c

def op(ea, n):
	'''Returns a tuple describing a specific operand of an instruction'''
	return (idc.GetOpType(ea, n), idc.GetOperandValue(ea, n))


if __name__ == '__main__':
	main()
