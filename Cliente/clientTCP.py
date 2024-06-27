import socket
import hashlib

SERVIDOR_IP = 'localhost'  
SERVIDOR_PORTA = 50000  

def calcular_hash(arquivo):
    hash_md5 = hashlib.md5()
    with open(arquivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def cliente_tcp():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        cliente.connect((SERVIDOR_IP, SERVIDOR_PORTA))
        print(f"Conectado ao servidor {SERVIDOR_IP}:{SERVIDOR_PORTA}")

        while True:

            mensagem = input("Insira a requisição:\narquivo nome.ext - Solicitar arquivo\nsair - Encerrar conexão\nchat - Exibir chat\n")
            
            cliente.send(mensagem.encode())

            if mensagem.lower() == 'sair':
                print("Desconectando do servidor...")
                break
            elif mensagem.lower().startswith("arquivo"):
                resposta = cliente.recv(1024).decode()
                if resposta == "OK":
                    hash_servidor = cliente.recv(1024).decode()
                    nome_arquivo = mensagem.split(' ', 1)[1]
                    with open(nome_arquivo, 'wb') as file:
                        while True:
                            data = cliente.recv(1024)
                            if data.endswith(b"SUCESSO"):
                                file.write(data[:-7])  
                                print("Arquivo recebido com sucesso")
                                break
                            file.write(data)
                    
                    hash_cliente = calcular_hash(nome_arquivo)
                    if hash_cliente == hash_servidor:
                        print("Integridade do arquivo verificada com sucesso")
                    else:
                        print("Erro: O hash do arquivo não corresponde")
                else:
                    print(resposta)
            elif mensagem.lower() == 'chat':
                resposta_chat = cliente.recv(1024).decode()
                print(f"Servidor: {resposta_chat}")
                while True:
                    mensagem_chat = input("Você: ")
                    cliente.send(mensagem_chat.encode())
                    if mensagem_chat.lower() == 'sair':
                        resposta_chat = cliente.recv(1024).decode()
                        print(f"Servidor: {resposta_chat}")
                        break
                    resposta_chat = cliente.recv(1024).decode()
                    print(f"Servidor: {resposta_chat}")               
            else:
                resposta = cliente.recv(1024).decode()
                print("Resposta do servidor:", resposta)

    except Exception as e:
        print(f"Erro na conexão: {e}")

    finally:

        cliente.close()

if __name__ == "__main__":
    cliente_tcp()
