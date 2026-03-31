#!/usr/bin/env python3
import socket
import threading
import select
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler
import struct
import configparser
import os

def load_config(config_file='config.txt'):
    """Load configuration from file"""
    config = configparser.ConfigParser()
    
    # Check if config file exists
    if not os.path.exists(config_file):
        print(f"❌ Configuration file '{config_file}' not found!")
        print("Please create config.txt with the following format:")
        print("""
[MTProto]
MT_PROXY_HOST = your_mtproto_proxy_ip
MT_PROXY_PORT = 443
MT_PROXY_SECRET = your_mtproto_secret

[SOCKS5]
SOCKS5_HOST = 127.0.0.1
SOCKS5_PORT = 1080
        """)
        exit(1)
    
    try:
        # Read the config file
        config.read(config_file)
        
        # Check if sections exist
        if 'MTProto' not in config:
            raise Exception("Missing [MTProto] section")
        if 'SOCKS5' not in config:
            raise Exception("Missing [SOCKS5] section")
        
        # Load MTProto settings
        mt_host = config['MTProto'].get('MT_PROXY_HOST')
        mt_port = config['MTProto'].getint('MT_PROXY_PORT')
        mt_secret = config['MTProto'].get('MT_PROXY_SECRET')
        
        # Load SOCKS5 settings
        socks5_host = config['SOCKS5'].get('SOCKS5_HOST')
        socks5_port = config['SOCKS5'].getint('SOCKS5_PORT')
        
        # Validate settings
        if not mt_host or not mt_secret:
            raise Exception("Missing MTProto settings")
        if not socks5_host or not socks5_port:
            raise Exception("Missing SOCKS5 settings")
        
        return {
            'mt_host': mt_host,
            'mt_port': mt_port,
            'mt_secret': mt_secret,
            'socks5_host': socks5_host,
            'socks5_port': socks5_port
        }
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        exit(1)

class MTProtoProxy:
    def __init__(self, host, port, secret):
        self.host = host
        self.port = port
        self.secret = secret.encode('utf-8')
        self.conn = None
        
    def connect(self):
        """Connect to MTProto server"""
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        self.conn.sendall(self.secret)
        
    def forward(self, data):
        """Send data to MTProto proxy and receive response"""
        self.conn.sendall(data)
        return self.conn.recv(4096)

class Socks5Handler(StreamRequestHandler):
    def handle(self):
        # Get configuration from class attribute
        config = self.server.config
        
        mt_proxy = MTProtoProxy(config['mt_host'], config['mt_port'], config['mt_secret'])
        mt_proxy.connect()
        
        # SOCKS5 handshake
        version, nmethods = struct.unpack('!BB', self.connection.recv(2))
        methods = self.connection.recv(nmethods)
        self.connection.sendall(struct.pack('!BB', 0x05, 0x00))
        
        # SOCKS5 request
        version, cmd, _, addr_type = struct.unpack('!BBBB', self.connection.recv(4))
        
        if addr_type == 0x01:  # IPv4
            addr = socket.inet_ntoa(self.connection.recv(4))
        elif addr_type == 0x03:  # Domain name
            domain_length = ord(self.connection.recv(1))
            addr = self.connection.recv(domain_length)
        else:
            self.connection.close()
            return
            
        port = struct.unpack('!H', self.connection.recv(2))[0]
        
        # Send SOCKS5 response
        self.connection.sendall(struct.pack('!BBBBIH', 0x05, 0x00, 0x00, 0x01, 
                                       0x00000000, 0x0000))
        
        try:
            while True:
                r, _, _ = select.select([self.connection, mt_proxy.conn], [], [])
                
                if self.connection in r:
                    data = self.connection.recv(4096)
                    if not data:
                        break
                    response = mt_proxy.forward(data)
                    if not response:
                        break
                    self.connection.sendall(response)
                
                if mt_proxy.conn in r:
                    data = mt_proxy.conn.recv(4096)
                    if not data:
                        break
                    self.connection.sendall(data)
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.connection.close()
            mt_proxy.conn.close()

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True
    config = None  # Class attribute to store configuration

def main():
    # Load configuration
    config = load_config()
    
    print(f"🚀 SOCKS5 proxy running on {config['socks5_host']}:{config['socks5_port']}")
    print(f"🔗 Connected to MTProto proxy: {config['mt_host']}:{config['mt_port']}")
    
    # Create server with configuration
    server = ThreadedTCPServer((config['socks5_host'], config['socks5_port']), Socks5Handler)
    server.config = config  # Store config in server instance
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Stopping server...")
        server.shutdown()

if __name__ == "__main__":
    main()
