# Trabalho 1 - Multithreaded Python Socket Server
##  Marcos Vinícius Porto de Sá

### Instalando o servidor e testando
```
git clone https://github.com/marcosvporto/INF1407-trabalho1.git
```
 1. Na pasta raíz edite o arquivo **_configuracao.py_** conforme descrito nos comentários do arquivo.

 2. Execute o arquivo **_server.py_** no terminal ou na linha de comando.
```
python server.py
```
_ou_
```
python3 server.py
```
_ou_
```
py server.py
```

3. Acesse o servidor a partir de um browser Firefox ou Chrome.
```
localhost:porta/nomedoarquivo.extensao
```
_ou_
```
localhost:porta/subpasta/nomedoarquivo.extensao
```

### Relatório

**Testes**
- Ao acessar arquivos presentes no diretório raiz :: Comportamento Esperado
- Ao acessar arquivos ausentes no diretório raiz e com pelo menos 1 arquivo da lista padrão presente no diretório em qualquer indice da lista :: Comportamento Esperado 
- Ao acessar arquivos ausentes no diretório raiz e com nenhum arquivo da lista padrão presente no diretório em qualquer indice da lista :: Comportamento Esperado
- Ao configurar incorretamente o módulo de configuração :: Comportamento Esperado
- Ao acessar arquivos html com referência a um código Javascript :: Comportamento Inesperado (Não Resposta) 