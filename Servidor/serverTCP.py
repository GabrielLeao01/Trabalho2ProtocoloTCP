import socket

MEU_IP = ''
MINHA_PORTA = 50000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

chat = ["Historico chat \n"]
servidor = (MEU_IP, MINHA_PORTA)
tcp.bind(servidor)
print("Servidor rodando")
tcp.listen(1)

while True:
    conexao, ip_cliente = tcp.accept()
    print("O cliente ", ip_cliente, "se conectou")
    
    while True:
        requisicao = conexao.recv(1024).decode()
        if not requisicao:
            break
        chat.append(requisicao + "\n")
        
        if requisicao == 'sair':
            print("O cliente ",ip_cliente,"se desconectou")
            break
        elif requisicao.startswith("arquivo"):
            arquivo = requisicao.split(' ', 1)[1]
            try:
                with open(arquivo, 'rb') as file:
                    conexao.send(b"OK")
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        conexao.send(data)
                file.close()
                conexao.send(b"SUCESSO")
                print("Arquivo enviado")
            except FileNotFoundError:
                conexao.send(b"Erro: Arquivo nao encontrado")
        elif requisicao == 'chat':
            for linha in chat:
                conexao.send(linha.encode())
            print("Historico de chat enviado")
    
    conexao.close()
