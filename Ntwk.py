import ssl, socket
from datetime import datetime
from OpenSSL import rand, crypto, SSL
from urlparse import urlparse

txt2 = open("histogram.csv", "a")

for folderName in os.listdir("certs"):
    path = s.path.join("certs", folderName, "analysis.txt")
    with open(path, "r") as file:
        txt = open(s.path.join("certs", folderName, "certs.txt"), "a")
        for line in file:
            if(line.find("Found URL: ") != -1):
                s = line.replace("Found URL: ", "")
                try:
                    parsed_uri = urlparse(s)
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
                    pass
        txt.close()
txt2.close()



