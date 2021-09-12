from socket import *
from configuracao import DEFAULT_FILES, PORT, FILE_PATH, ERROR_PAGE
from sys import exit
def getEnderecoHost(porta): 
    try: 
        enderecoHost = getaddrinfo( 
            None,  
            porta,              
            family=AF_INET,              
            type=SOCK_STREAM,              
            proto=IPPROTO_TCP,  
            flags=AI_ADDRCONFIG | AI_PASSIVE)
    except:         
        print("Não obtive informações sobre o servidor (???)", file=stderr) 
        abort()     
    return enderecoHost

def criaSocket():
    return socket(AF_INET, SOCK_STREAM)


def setModo(fd): 
    fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    return

def bindaSocket(fd, porta): 
    try: 
        fd.bind(('', porta)) 
    except Exception as exc: 
        print("Erro ao dar bind no socket do servidor") 
        print(exc)
        exit()     
    return

def escuta(fd):
    try: 
        fd.listen(0) 
    except Exception as exc: 
        print("Erro ao começar a escutar a porta")
        print(exc)
        exit()    
    print("Iniciando o serviço"); 
    return

def conecta(fd): 
    (con, cliente) = fd.accept() 
    print("Servidor conectado com", cliente) 
    return con
def handlePageNotFound(clientsocket, indice):
    print(indice)
    if indice < len(DEFAULT_FILES):
        arquivo = DEFAULT_FILES[indice]
        extensao = arquivo.split(".")[-1]
        handleRequest(clientsocket, arquivo, extensao, indice)
    else:
        try:
            data = open(FILE_PATH+ERROR_PAGE, mode="r", encoding="utf-8").read()
            content =  "HTTP/1.1 404 PageNotFound\r\n"
            content += "Content-Type: text/html; charset=utf-8\r\n"
            content += "\r\n"
            content += data     
            clientsocket.send(content.encode("utf-8"))
            clientsocket.shutdown(SHUT_WR)
        except OSError:
            print("Página não encontrada:\n")
            return
            
    return
    


def handleRequest(clientsocket, arquivo, extensao,indice=0):
    if extensao.upper() in ["JPEG", "JPG", "PNG" , "GIF"]:
        try:
            data = open(FILE_PATH+arquivo, "r+b").read()
            clientsocket.send('HTTP/1.1 200 OK\r\n'.encode())
            clientsocket.send("Content-Type: image/{ext}\r\n".format(ext=extensao).encode())
            clientsocket.send("Accept-Ranges: bytes\r\n\r\n".encode())
            clientsocket.send(data)
            clientsocket.shutdown(SHUT_WR)
        except OSError:
            print("Página não encontrada", arquivo)
            handlePageNotFound(clientsocket,indice+1)
                
    elif extensao.upper() in ["HTML", "JS"]: 
        try:
            data = open(FILE_PATH+arquivo, mode="r", encoding="utf-8").read()
            content =  "HTTP/1.1 200 OK\r\n"
            content += "Content-Type: text/{fileExt}; charset=utf-8\r\n".format(fileExt=extensao.lower())
            content += "\r\n"
            content += data     
            clientsocket.send(content.encode("utf-8"))
            clientsocket.shutdown(SHUT_WR)
        except OSError:
            print("Página não encontrada", arquivo)
            handlePageNotFound(clientsocket,indice+1)
            
    else:
        handlePageNotFound(clientsocket,indice) 
    return

def main():
    enderecoHost = getEnderecoHost(PORT)
    print(enderecoHost)
    serversocket = criaSocket()
    setModo(serversocket)
    bindaSocket(serversocket, PORT)
    print("Servidor pronto em {server}:{port}".format(server = enderecoHost, port = PORT))
    escuta(serversocket)
    try:
        while (True):
            clientsocket = conecta(serversocket)
            request = clientsocket.recv(5000).decode("utf-8")
            pieces = request.split("\n")
            if (len(pieces) > 0):
                for param in pieces: 
                    if param.split(":")[0] == "Sec-Fetch-Mode":
                        if "navigate" in param.split(":")[1]:
                            arquivo = pieces[0].split(" ")[1][1:]
                            extensao = arquivo.split(".")[-1].upper()
            handleRequest(clientsocket, arquivo, extensao)               
    except Exception as exc:
        print("Error handling connection:\n")
        print(exc)
    clientsocket.close()
    return

if __name__ == '__main__':
    main()