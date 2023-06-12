################################################
# sslwebserver.py
# PA4 webserver script
# Modified from Lab 6 by Anna Bellizzi
################################################

#!/usr/bin/env python3
import http.server
import ssl
 
## Variables you can modify
#server_address = "ca.cst311.test"
server_address = "www.webpa4.test"
server_port = 4443
ssl_key_file = "/etc/ssl/demoCA/private/cst311.webpa4-key.pem"
ssl_certificate_file = "/etc/ssl/demoCA/newcerts/cst311.webpa4-cert.pem"
 
 
## Don't modify anything below
httpd = http.server.HTTPServer((server_address, server_port), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket,
                server_side=True,
                                keyfile=ssl_key_file,
                                certfile=ssl_certificate_file,
                ssl_version=ssl.PROTOCOL_TLSv1_2)
 
print("Listening on port", server_port)                                
httpd.serve_forever()
