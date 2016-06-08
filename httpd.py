#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import base64
import os
import subprocess
import sys
import time

#https://github.com/tanzilli/playground/blob/master/python/httpserver/example3.py
PORT_NUMBER = 8000

#This class will handles any incoming request from
#the browser 


class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		sendReply = False
		print "GET  Method"
		if self.path=="/":
		   self.path="/index.html"
               
                if self.path == "/api/led":
		    self.path ="/led.db"
		    mimetype='application/json'
		    sendReply = True								
		try:
			#Check the file extension required and
			#set the right mime type

			
			#sendReply = True
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		print "POST Method"
 		varLen = int(self.headers['Content-Length'])
    		postBody = self.rfile.read(varLen)
                print postBody
		repBody = ""
		print self.path
		if  self.path.find("datatobase64") !=-1:
			#Encode as Base64
			repBody  = base64.b64encode(postBody)
		elif self.path.find("base64todata") !=-1:
			repBody  =  base64.b64decode(postBody)
		elif self.path.find("/compile/python") !=-1:
			 hFile = open("test.py", 'wb')
			 hFile.write("%s" % (postBody)) 
			 hFile.close()
			 print "Run the command line and store file"

			 os.system('python test.py >> text.txt')
			 time.sleep(0.1)
			 print "Reading file"
			 f = open('./text.txt')
			 repBody = f.read()
			 f.close()
			 os.remove("./text.txt")
		elif  self.path =="/api/led":
  			self.send_response(200)
			self.send_header('Content-Length','0') 
			self.end_headers()
			print "store DB"
			hFile = open("./led.db", 'wb')
 			hFile.write("%s" % (postBody))
                        hFile.write("%s",'\0') 
			hFile.close()
			return 
		else :
			repBody ="Unspport uil="+self.path;
		
		
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write(repBody)		
		print "Send the html message"
		print repBody
#try:
	#Create a web server and define the handler to manage the
	#incoming request
server = HTTPServer(('', PORT_NUMBER), myHandler)
print 'Started httpserver on port ' , PORT_NUMBER
while True:
	#Wait forever for incoming htto requests
	server.serve_forever()
#server.socket.close()

#except KeyboardInterrupt:
	#print '^C received, shutting down the web server'
	#server.socket.close()

"""			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
"""
	

