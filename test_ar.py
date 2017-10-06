import unix_ar
import fat_lipo

#fat_lipo.extractARMv7('/Users/illyasigov/Downloads/lib.a', '/Users/illyasigov/Downloads/gib.a')
ar = unix_ar.Archive('/Users/illyasigov/Downloads/gib.a')
#ar.extractall('/Users/illyasigov/Downloads/')
ar.read_all_headers()
for f in ar.archived_files.keys():
	print(f + "\n")
	#out_path = output + "/" + f
	#with open(out_path.rstrip('\0'), 'wb') as wf: 
		#wf.write(ar.archived_files[f].read())