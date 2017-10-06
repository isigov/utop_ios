from idc import *
from idaapi import *
from idautils import *
import idc
import ssl, socket
from datetime import datetime
from OpenSSL import rand, crypto, SSL
from urlparse import urlparse

txt = None
swift = False

def imp_cb(ea, name, ord):
    global swift
    if name:
        if(name.find("swift") != -1):
                swift = True
                return False

    return True

sc = Strings()
aws_count = 0
http_count = 0
folderName = idaapi.get_root_filename() + "_analysis"
os.makedirs(os.path.join("certs", folderName))
txt = open(os.path.join("certs", folderName, "analysis.txt"), "a")
txt2 = open("histogram.csv", "a")
txt.write("=" + idaapi.get_root_filename() + "=\n")
for s in sc:
        if(str(s).find("AKIA") != -1):
                txt.write("Found AWS token: %s\n" % (str(s)))
                aws_count+=1
        if(str(s).find("http://") != -1):
                txt.write("Found URL: %s\n" % (str(s)))
                http_count+=1
        if(str(s).find("https://") != -1):
                res = ""
                try:
                        parsed_uri = urlparse(str(s))
                        hostname = '{uri.netloc}'.format(uri=parsed_uri)
                        cert = ssl.get_server_certificate((hostname, 443), ssl_version=ssl.PROTOCOL_TLSv1)
                        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
                        res = x509.get_subject().get_components()
                        expire_date = datetime.strptime(x509.get_notAfter(), "%Y%m%d%H%M%SZ")
                        expire_in = expire_date - datetime.now()
                        open(os.path.join("certs", folderName, "cert.crt"), "wt").write(cert)
                        txt2.write("%d\n" % (expire_in.days))
                        txt.write("Found URL: %s\nExpires in: %d days\nExpiration date: %s\nOther: %s\n" % (str(s), expire_in.days, expire_date.strftime('%m/%d/%Y'), res))
                except:
                        txt.write("Found URL %s\n" % (str(s)))
                        pass    
                http_count+=1

nimps = idaapi.get_import_module_qty()
for i in xrange(0, nimps):
    idaapi.enum_import_names(i, imp_cb)

if(swift == True):
        txt.write("App uses swift!\n")
else:
        txt.write("App doesn't use swift!\n")
        
txt.write("Found %d tokens, %d URLs\n\n" % (aws_count, http_count))
txt2.close()
txt.close()
idc.Exit(0)
