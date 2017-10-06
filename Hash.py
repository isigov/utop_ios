from idc import *
from idaapi import *
from idautils import *
import os
import hashlib
import re

def main():
    first_ea = BeginEA()
    #print("[DEBUG] Starting to hash file %s\n" % (get_root_filename()))

    text_file = open("Output.txt", "w")

    #for ea in Segments():
    for funcea in Functions(SegStart(first_ea), SegEnd(first_ea)):
        #functionName = GetFunctionName(funcea)
        #print("[DEBUG] Moving to function %s" % (hex(funcea)))
        concat = ""
        instr_count = 0
        for (startea, endea) in Chunks(funcea):
            for head in Heads(startea, endea):
                opnum = op_count(head)
                name = GetMnem(head)
                for i in range(0, opnum):
                    optype, val = op(head, i)
                    #val2 = GetOpnd(head, i)
                    if(optype == 1):
                        name = name + " R,"
                    else:
                        name = name + " ADDR,"
                    #elif(optype in (2, 3, 4, 6, 7)):
                    #    name = name + " ADDR,"
                    #else:
                    #    name = name + " {0},".format(str(val))
                #print("[DEBUG] Intruction is %s\n" % name)

                #instr = GetDisasm (head)
                #instr = re.sub('R\d', 'R', instr)
                #print("[DEBUG] Disassembled instruction: %s" % (instr))
                concat = concat + name
                instr_count = instr_count + 1
        if(instr_count > 10):
            m = hashlib.md5()
            m.update(concat)
            my_hash = m.hexdigest()
            #print("[DEBUG] Created hash %s for function %s\n" % (my_hash, hex(funcea)))
            text_file.write("%s, %d, %s, %d, %d\n" % (my_hash, int(get_root_filename().replace(".bin", "")), GetFunctionName(funcea), funcea, instr_count))
        
        #print("python ./Hash_DB.py {0} {1} {2}".format(my_hash, get_root_filename(), functionName))

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