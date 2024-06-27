import socket
import threading
import hashlib

MEU_IP = ''
MINHA_PORTA = 50000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind((MEU_IP, MINHA_PORTA))
tcp.listen(5)

print("Servidor rodando")

def calcular_hash(arquivo):
    hash_md5 = hashlib.md5()
    with open(arquivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def handle_client(conexao, ip_cliente):
    print("O cliente ", ip_cliente, "se conectou")
    while True:
        try:
            requisicao = conexao.recv(1024).decode()
            if not requisicao:
                break
            if requisicao == 'sair':
                print("O cliente ", ip_cliente, "se desconectou")
                break
            elif requisicao.startswith("arquivo"):
                arquivo = requisicao.split(' ', 1)[1]
                try:
                    with open(arquivo, 'rb') as file:
                        conexao.send(b"OK")
                        hash_arquivo = calcular_hash(arquivo)
                        conexao.send(hash_arquivo.encode())
                        while True:
                            data = file.read(1024)
                            if not data:
                                break
                            conexao.send(data)
                    conexao.send(b"SUCESSO")
                    print(f"Arquivo enviado para cliente {ip_cliente}")
                except FileNotFoundError:
                    conexao.send(b"Erro: Arquivo nao encontrado")
            elif requisicao == 'chat':
                conexao.send(b"Modo chat ativado")
                while True:
                    mensagem = conexao.recv(1024).decode()
                    if mensagem == 'sair':
                        conexao.send(b"Modo chat desativado")
                        break
                    print(f"Cliente {ip_cliente}: {mensagem}")
                    resposta = input("Resposta para o cliente: ")
                    conexao.send(resposta.encode())

        except Exception as e:
            print(f"Erro na conexão com {ip_cliente}: {e}")
            break
    
    conexao.close()

while True:
    conexao, ip_cliente = tcp.accept()
    client_thread = threading.Thread(target=handle_client, args=(conexao, ip_cliente))
    client_thread.start()
