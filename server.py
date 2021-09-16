from socket import *
from configuracao import DEFAULT_FILES, PORT, FILE_PATH, ERROR_PAGE
from sys import exit
from _thread import *
from time import sleep
import threading

conexoesSimultaneas = 0
lock = threading.Lock()

'''
tarefa 
Função a ser executada dentro de uma nova thread
Já assume que uma conexão com o cliente foi estabelecida
Recebe o socket e o endereço do cliente
Fica num loop infinito esperando receber uma mensagem do socket do cliente
Foi feito uma filtragem na mensagem recebida para validar se é uma chamada HTTP contendo a solicitação do 
arquivo
Observando os parâmetros das requisições GET dos Browsers foi observado que o endereço solicitado apenas 
aparece quando a chave Sec-Fetch-Mode possui o valor navigate
Quando estamos lidando de fato com uma requisição que solicita o arquivo presente na URL, chamamos a função
handleRequest, impementada a seguir neste documento, passando o socket do cliente, o caminho do arquivo 
e sua extensao
Após a execução da handleRequest, encerramos a conexão com o cliente

 
'''

def tarefa(clientsocket, clientaddress):
    global conexoesSimultaneas
    while True:
        request = clientsocket.recv(1024).decode("utf-8")
        if not request:
            break
        pieces = request.split("\n")
        arquivo=""
        extensao=""
        if (len(pieces) > 0):
            for param in pieces: 
                if param.split(":")[0] == "Sec-Fetch-Mode":
                    if "navigate" in param.split(":")[1]:
                        arquivo = pieces[0].split(" ")[1][1:]
                        extensao = arquivo.split(".")[-1].upper()
                        handleRequest(clientsocket, arquivo, extensao)
    
    sleep(10) # Teste do Multithreading :: Remover para comportameto normal da aplicacao
    print("Servidor desconectado de", clientaddress)
    lock.acquire()
    conexoesSimultaneas -= 1
    lock.release()
    print("%d Conexoes Simultanes" %conexoesSimultaneas)
    clientsocket.close()
    return 

'''
criaSocket
visto em sala
'''
def criaSocket():
    return socket(AF_INET, SOCK_STREAM)


'''
setMetodo
visto em sala
'''
def setModo(fd): 
    fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    return

'''
bindaSocket
visto em sala
'''
def bindaSocket(fd, porta): 
    try: 
        fd.bind(('', porta)) 
    except Exception as exc: 
        print("Erro ao dar bind no socket do servidor") 
        print(exc)
        exit()     
    return


'''
escuta
visto em sala
'''
def escuta(fd):
    try: 
        fd.listen(5) 
    except Exception as exc: 
        print("Erro ao começar a escutar a porta")
        print(exc)
        exit()    
    print("Iniciando o serviço"); 
    return

'''
conecta
visto em sala
incrementa a variável conexoesSimultaneas para testar o multithreading
'''

def conecta(fd): 
    global conexoesSimultaneas
    (con, cliente) = fd.accept() 
    conexoesSimultaneas +=1
    print("Servidor conectado com", cliente) 
    print("%d Conexoes Simultanes" %conexoesSimultaneas)
    return (con, cliente)


'''
handlePageNotFound
É invocada pela função handleRequest quando esta não consegue abrir o documento requerido na URL do metodo
GET do cliente
Chama a função handleRequest de forma recursiva passando o socket do cliete, o indice da lista recebido, 
o caminho e nome do arquivo presente na lista dos arquivos padrões do módulo de configuração, 
referente ao indice da lista recebido, e a extensão do arquivo correspondente 
Se o indice recebido estiver fora da lista, a página de error 404 padrão presente no módulo de configuração
é exibida 
Assume-se que a página de erro será no formato html
'''
def handlePageNotFound(clientsocket, indice):
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
    

'''
handleRequest

Recebe o socket do cliente, o caminho e nome do arquivo, sua extensão e um indice
o indicie é utilizado para saber qual é o indice da lista de arquivos padrão presente no módulo de 
configuração deverá ser usado caso não seja possível acessar o arquivo solicitado
a resposta ao cliente dependerá da extensão do arquivo
se o arquivo solicitado for imagem ou gif, lemos os bytes e retornamos ao cliente a mensagem fragmentada
pois não é possivel concatenar bytes com array em python

Se o arquivo solicitado for de texto (HTML, JS) podemos enviar toda a resposta de uma vez codficada em utf-8

caso não seja possível abrir o arquivo solicitado,ou caso o arquivo solicitado venha sem extensao, 
a função handleePageNotFound é chamada

a cada vez que chamamos ahandlePageNotFound incrementamos o indice solicitado, para percorrer todos os
indices da lista de arquivops padrão presente no módulo de configuração antes que enviemos a página de 
erro 404

'''
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
    if not (isinstance(DEFAULT_FILES, list)  and isinstance(PORT,int)  and isinstance(FILE_PATH,str) and isinstance(ERROR_PAGE,str)):
        print("Módulo de Configuração Inconsistente")
        exit()
    serversocket = criaSocket()
    setModo(serversocket)
    bindaSocket(serversocket, PORT)
    print("Servidor pronto em http://localhost:{}".format(PORT))
    escuta(serversocket)
    try:
        while (True):
            (clientsocket, clientaddress) = conecta(serversocket)
            t1 = threading.Thread(target = tarefa, args=(clientsocket,clientaddress))
            t1.start()       
    except Exception as exc:
        print("Error handling connection:\n")
        print(exc)
    
    
    return

if __name__ == '__main__':
    main()