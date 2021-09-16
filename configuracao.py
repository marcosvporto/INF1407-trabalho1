'''
DEFAULT_FILES lista de páginas a serem exibidas caso a página requisitada não seja encontrada
Ex:
['pagina1.html','pagina2.jpg','pagina3.gif']
'''
DEFAULT_FILES = ['background1.jpg','background2.jpg','calculadora.html']


'''
PORT porta a escutar as requisições do cliente
Ex:
80 ou 8080
'''
PORT  = 8080


'''
FILE_PATH diretório raiz onde estarão armazenados os arquivos a serem solicitados e enviados
Ex:
'/home/Documents/views/'
"C:/User/username/Documents/views/"
'''
FILE_PATH = "C:/Users/marco/Desktop/INF1407/trabalho1/views/"


'''
ERROR_PAGE
página a ser exeibida caso não seja possível exibir tanto a página solicitada quanto as páginas presentes 
na lista DEFAULT_FILES

Ex:
'pagenotfound.html'

'''
ERROR_PAGE = 'pagenotfound.html'