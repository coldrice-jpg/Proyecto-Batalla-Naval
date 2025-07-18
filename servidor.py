import socket
import json
import logging

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Server:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ""
        self.port = 0
        self.addr = None
        self.connection = None

    def iniciar_server(self, host, port):
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.client.bind(self.addr)
        self.client.listen(1)
        logging.info(f"Servidor iniciado en {self.host}:{self.port}, esperando conexión...")
        return True

    def aceptar_conexion(self):
        try:
            self.client.settimeout(0.5) 
            conn, addr = self.client.accept()
            self.connection = conn
            self.connection.setblocking(False)
            logging.info(f"Conexión aceptada desde {addr}")
            return True
        except socket.timeout:
            return False 

    def conectar_server(self, host, port):
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        try:
            self.client.connect(self.addr)
            self.connection = self.client
            self.connection.setblocking(False) 
            logging.info(f"Conectado al servidor en {self.addr}")
            return True
        except socket.error as e:
            logging.error(f"No se pudo conectar: {e}")
            return False

    def enviar(self, data):
        if not self.connection:
            return
        try:
            json_data = json.dumps(data)
            message = json_data.encode('utf-8')
            

            header = len(message).to_bytes(4, 'big')
            self.connection.sendall(header + message)
            
        except socket.error as e:
            logging.error(f"Error al enviar datos: {e}")

    def recibir(self):
        if not self.connection:
            return None
        try:
            header = self.connection.recv(4)
            if not header:
                return None
            
            msg_len = int.from_bytes(header, 'big')

            data = self.connection.recv(msg_len)
            if not data:
                return None

            return json.loads(data.decode('utf-8'))
            
        except BlockingIOError:
            return None 
        except (ConnectionResetError, json.JSONDecodeError) as e:
            logging.error(f"Error al recibir datos o conexión cerrada: {e}")
            self.connection = None 
            return None