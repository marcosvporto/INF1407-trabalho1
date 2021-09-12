from socket import *
from os import path, stat
from base64 import b64encode
from configuracao import DEFAULT_FILES, PORT, FILE_PATH, ERROR_PAGE

def handleRequest(fileName, fileExtension):
    content = open(FILE_PATH+ERROR_PAGE, mode="r", encoding="utf-8").read()
    if fileExtension.upper() in ["HTML", "JS"]:
        try:
            content = open(FILE_PATH+fileName, mode="r", encoding="utf-8").read()
        except Exception as exc:
            print("Error while trying to open text file:\n")
            print(exc)
        data =  "HTTP/1.1 200 OK\r\n"
        data += "Content-Type: text/{fileExt}; charset=utf-8\r\n".format(fileExt=fileExtension.lower())
        data += "\r\n"
        data += content
    elif fileExtension.upper() in  ["JPEG", "JPG", "PNG" , "GIF"]:
        try:
            size = str(stat(FILE_PATH+fileName).st_size)
            content = open(FILE_PATH+fileName, "r+b").read()
            encoded_string = b64encode(content) 
        except Exception as exc:
            print("Error while trying to open image file:\n")
            print(exc)
        data = content
    else:
        data =  "HTTP/1.1 404 Not Found\r\n"
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "\r\n"
        data += content
    return data

def main():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(('localhost', PORT))
        serversocket.listen(5)
        while(1):
            (clientsocket, address) = serversocket.accept()
            rd = clientsocket.recv(5000).decode("utf-8")
            pieces = rd.split("\n")
            if (len(pieces) > 0) :
                print('pieces \n',pieces)
                print('\n')
                for param in pieces:
                 
                    if param.split(":")[0] == "Sec-Fetch-Mode":
                        #print(param.split(":")[1])
                        if "navigate" in param.split(":")[1]:
                            
                            #print(rd)
                            arquivo = pieces[0].split(" ")[1][1:]
                            #print('arquivo = ',arquivo)
                            extensao = arquivo.split(".")[-1].upper()
                            #print('extensao', extensao)
                            #data = handleRequest(arquivo,extensao)
            
            if extensao.upper() in ["JPEG", "JPG", "PNG" , "GIF"]:
                data = open(FILE_PATH+arquivo, "r+b").read()
                clientsocket.send('HTTP/1.1 200 OK\r\n'.encode())
                clientsocket.send("Content-Type: image/{ext}\r\n".format(ext=extensao).encode())
                clientsocket.send("Accept-Ranges: bytes\r\n\r\n".encode())
                clientsocket.send(data)
                clientsocket.shutdown(SHUT_WR)
            elif extensao.upper() in ["HTML", "JS"]: 
                try:

                    data = open(FILE_PATH+arquivo, mode="r", encoding="utf-8").read()
                except Exception as exc:
                    print("Error while trying to open text file:\n")
                    print(exc)
                content =  "HTTP/1.1 200 OK\r\n"
                content += "Content-Type: text/{fileExt}; charset=utf-8\r\n".format(fileExt=extensao.lower())
                content += "\r\n"
                content += data     
                #clientsocket.send('HTTP/1.1 200 OK\r\n'.encode())
                #clientsocket.send("Content-Type: text/{ext}\r\n; charset=utf-8".format(ext=extensao).encode())
                clientsocket.send(content.encode("utf-8"))
                clientsocket.shutdown(SHUT_WR)

    except Exception as exc:
        print("Error trying to encode data:\n")
        print(exc)
    serversocket.close()

if __name__ == '__main__':
    main()