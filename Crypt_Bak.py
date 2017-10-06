from idc import *
from idaapi import *
from idautils import *
import os

recursion_depth = 0

def recursive(ea, startea, endea, fil):
    global recursion_depth
    for xref in XrefsTo(ea, 0):
        if(xref.frm > startea and endea > xref.frm):
            fil.write("Found string in fcn using CCCrypt: %s\n" % (str(s)))
            break
        else:
            if(recursion_depth <= 1):
                recursive(xref.frm, startea, endea, fil)
                recursion_depth = recursion_depth + 1

        
crypt = False
func_ea = 0
first_ea = BeginEA()
func_list = []

#print "====CCCrypt References By Illya====\n"

for ea in Segments():
    for funcea in Functions(SegStart(ea), SegEnd(ea)):
        functionName = GetFunctionName(funcea)
        if(functionName.find("_CCCrypt") != -1):
            func_ea = funcea
            crypt = True
            #print("[DEBUG] Found CCCrypt at %x\n" % func_ea)
        

if(crypt):
    folderName = get_root_filename() + "_cccrypt"
    os.makedirs(os.path.join("cccrypt", folderName))
    txt = open(os.path.join("cccrypt", folderName, "analysis.txt"), "a")
    for xref in XrefsTo(func_ea, 0):
        #print("[DEBUG] Found reference to CCCrypt at %x\n" % xref.frm)
        for funcea in Functions(SegStart(first_ea), SegEnd(first_ea)):
            for (startea, endea) in Chunks(funcea):
                #print("[DEBUG] Found function starting at %x and ending at %x\n" % (startea, endea))
                if(xref.frm > startea and endea > xref.frm):
                    #print("[DEBUG] Found function containg CCCrypt reference starting at %x and ending at %x\n" % (startea, endea))
                    func_list.append([startea, endea])
    sc = Strings()
    for [startea, endea] in func_list:
        for s in sc:
            recursive(s.ea, startea, endea, txt)
            recursion_depth = 0
    txt.close()

idc.Exit(0)
                
        
        
