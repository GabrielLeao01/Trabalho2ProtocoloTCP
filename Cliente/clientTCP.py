import socket

ip_servidor = 'localhost'
porta_servidor = 50000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((ip_servidor, porta_servidor))

print('Conectado\n')
while True:
    print("Insira a requisição:\narquivo nome.ext - Solicitar arquivo\nsair - Encerrar conexão\nchat - Exibir chat")
    requisicao = input()
    tcp.send(requisicao.encode())

    if requisicao.startswith('arquivo'):
        resposta = tcp.recv(1024)
        if resposta == b"Erro: Arquivo nao encontrado":
            print(resposta.decode())
        elif resposta == b"OK":
            arquivo = requisicao.split(' ', 1)[1]
            with open(arquivo, 'wb') as file:
                while True:
                    data = tcp.recv(1024)
                    if data == b"SUCESSO":
                        break
                    file.write(data)
            print('Arquivo recebido')
    elif requisicao == 'sair':
        tcp.close()
        print('Conexão encerrada')
        break
    elif requisicao == 'chat':
        while True:
            data = tcp.recv(1024)
            if not data:
                break
            print(data.decode())
