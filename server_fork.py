## using fork system call 

import socket
import sys
import time
import os

host_dir = '.'

def python_server():
    port = 8080
    
    host = '127.0.0.1'
    bind_socket(host, port)


def bind_socket(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
	server.bind((host, port))
	yellow_color = '\033[93m'
        white_color = '\033[0m'
	gray_color = '\033[90m'
	print(yellow_color + "Serving Python_Server")
	print("Available on : http://127.0.0.1:%d"%port)
	print(white_color + "Hit CTRL-C to stop the server" + gray_color)
    except:
	port += 1
	bind_socket(host, port)
    serve(server)


def serve(server):
    while True:
        print("Waiting for new connection\n")
	server.listen(10)
	client_connection, address = server.accept()
	pid = os.fork()
	if(pid == 0):
	    server.close()
	    handle_request(client_connection, address)
	    client_connection.close()
	    os.exit(0)
	else:
	    client_connection.close()


def handle_request(client_connection, address):
	received_rqst = client_connection.recv(1024)
	print("Recived connection from:",address)
	received_contnt = bytes.decode(received_rqst)
	request_method = received_contnt.split(' ')[0]
	print("Requested method:",request_method)
	if(request_method == 'GET'):
	    request_file = received_contnt.split(' ')[1]
	    if(request_file == '/'):
                request_file = '/index.html'
	    request_file = host_dir + request_file
	    try:
	        fp = open(request_file, 'rb')
		response_data = fp.read()
		fp.close()
		content_type = content_type_(request_file)
		header = header_(200, content_type)
	    except:
		header = header_(400, 'text/html')
		response_data = b'<html><body><p> Error 404 File not found</p></body></html>'	
	    final_response = header.encode()
	    final_response += response_data
	    client_connection.send(final_response)
            time.sleep(30)
            client_connection.close()
        else:
	    print(request_method)
	    print("HTTP request method unknown")			
			

def header_(http_code, content_type):
    headr = ''
    if(http_code == 200):
	headr = 'HTTP/1.1 200 OK\n'
    elif(http_code == 404):
	headr = 'HTTP/1.1 404 File Not Found\n'
    date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    headr += 'Date:' + date + '\n'
    headr += 'Server: Python-http-server\n'
    headr += 'Content-Type:'+ content_type + '\n'
    headr += '\n'
    return headr


def content_type_(file_name):
    content_types = {'html': 'text/html',
				    'txt': 'text/txt',
			            'jpg': 'image/jpeg',
				    'png': 'image/png',
                                    'pdf': 'application/pdf',
				    'gif': 'image/gif',
				    'ico': 'icon/ico'}
    return content_types[file_name.split('.')[-1]]
			

		
python_server()


