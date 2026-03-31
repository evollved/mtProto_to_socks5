# SOCKS5 to MTProto Proxy Bridge

A lightweight SOCKS5 proxy server that forwards traffic through an MTProto proxy (like Telegram's MTProto proxy). This allows you to use any SOCKS5-compatible application (browsers, torrent clients, etc.) with your MTProto proxy.

## 📋 Features

- **SOCKS5 Protocol Support**: Compatible with any SOCKS5 client
- **MTProto Proxy Integration**: Connects to MTProto proxy servers
- **Multi-threaded**: Handles multiple connections simultaneously
- **Lightweight**: Minimal dependencies, pure Python implementation
- **Configurable**: Easy configuration via external file
- **Cross-platform**: Works on Linux, macOS, and Windows

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- An MTProto proxy server address and secret

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/socks5-mtproto-bridge.git
cd socks5-mtproto-bridge
```

2. Create a configuration file:
```bash
cp config.example.txt config.txt
```

3. Edit `config.txt` with your MTProto proxy details:
```ini
[MTProto]
MT_PROXY_HOST = your_mtproto_proxy_ip
MT_PROXY_PORT = 443
MT_PROXY_SECRET = your_mtproto_secret

[SOCKS5]
SOCKS5_HOST = 127.0.0.1
SOCKS5_PORT = 1080
```

### Running the Proxy

```bash
python3 main.py
```

You should see:
```
🚀 SOCKS5 proxy running on 127.0.0.1:1080
🔗 Connected to MTProto proxy: your_mtproto_proxy_ip:443
```

## ⚙️ Configuration

### config.txt Format

The configuration file uses INI format with two sections:

#### MTProto Section
| Parameter | Description | Example |
|-----------|-------------|---------|
| `MT_PROXY_HOST` | MTProto proxy server address | `192.168.1.100` or `proxy.example.com` |
| `MT_PROXY_PORT` | MTProto proxy port | `443` |
| `MT_PROXY_SECRET` | MTProto proxy secret key | `your_secret_here` |

#### SOCKS5 Section
| Parameter | Description | Example |
|-----------|-------------|---------|
| `SOCKS5_HOST` | SOCKS5 server listening address | `127.0.0.1` (local only) or `0.0.0.0` (all interfaces) |
| `SOCKS5_PORT` | SOCKS5 server listening port | `1080` |

### Example Configuration
```ini
[MTProto]
MT_PROXY_HOST = 123.456.78.90
MT_PROXY_PORT = 443
MT_PROXY_SECRET = ee1234567890abcdef1234567890abcdef

[SOCKS5]
SOCKS5_HOST = 127.0.0.1
SOCKS5_PORT = 1080
```

## 🔧 Usage

### Configure Your Applications

Set your applications to use SOCKS5 proxy:
- **Host**: `127.0.0.1`
- **Port**: `1080`
- **Type**: SOCKS5
- **Authentication**: None

#### Examples:

**Firefox:**
1. Settings → Network Settings → Manual proxy configuration
2. SOCKS Host: `127.0.0.1`
3. Port: `1080`
4. SOCKS v5

**Telegram Desktop:**
1. Settings → Advanced → Connection Type
2. Use custom proxy
3. Type: SOCKS5
4. Host: `127.0.0.1`
5. Port: `1080`

**Command line (using curl):**
```bash
curl --socks5 127.0.0.1:1080 https://api.telegram.org
```

### Testing the Proxy

You can test if the proxy is working:
```bash
curl --socks5 127.0.0.1:1080 https://httpbin.org/ip
```

## 🛠️ How It Works

1. The script starts a SOCKS5 proxy server on the specified address and port
2. When a client connects, it performs the SOCKS5 handshake
3. After the handshake, the script connects to the MTProto proxy
4. All traffic is forwarded bidirectionally between the client and MTProto proxy
5. The MTProto proxy handles the actual connection to Telegram or other services

```
[Client App] <--SOCKS5--> [This Proxy] <--MTProto--> [MTProto Proxy] <--> [Internet]
```

## 🔒 Security Considerations

- The proxy runs without authentication by default
- Consider using it only locally (127.0.0.1) or behind a firewall
- MTProto secret is transmitted in plain text to the proxy
- Use HTTPS when possible for end-to-end encryption

## 🐛 Troubleshooting

### Connection Issues

**Problem**: Can't connect to MTProto proxy
- Check if MT_PROXY_HOST and MT_PROXY_PORT are correct
- Verify the proxy is accessible from your network
- Check firewall settings

**Problem**: SOCKS5 handshake fails
- Ensure client is using SOCKS5 (not SOCKS4)
- Verify no authentication is required

**Problem**: Slow performance
- Try increasing buffer sizes in the code
- Check network latency to MTProto proxy

### Logs

The proxy logs errors to console. Run with:
```bash
python3 main.py
```

## 📊 Performance

- Supports multiple concurrent connections
- Each connection runs in its own thread
- Buffer size: 4096 bytes (configurable)
- Minimal memory footprint

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This software is for educational purposes only. Users are responsible for complying with local laws and regulations regarding proxy usage. The authors are not responsible for any misuse of this software.

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the configuration file format

## 🔄 Updates

Check for updates regularly:
```bash
git pull origin main
```

---

**Note**: This proxy does not provide encryption between the client and this proxy server. For secure communication, ensure your applications use HTTPS or other encryption protocols on top of the proxy connection.# mtProto_to_socks5
Convert mtproto proxy to socks5

# MTProto to SOCKS5 Conversion Script

Here is a complete Python script that converts an MTProto proxy to SOCKS5:

## Usage Guide

1. **Prerequisites Installation**:
   ```bash
   pip install pysocks
   ```

2. **Configuration**:
   - `MT_PROXY_HOST`: MTProto server address
   - `MT_PROXY_PORT`: Proxy port
   - `MT_PROXY_SECRET`: MTProto proxy secret key
   - `SOCKS5_HOST` and `SOCKS5_PORT`: Local address and port for SOCKS5

3. **Running the Script**:
   ```bash
   python3 mtproto_to_socks5.py
   ```

4. **Using the Proxy**:
   - Use `127.0.0.1:1080` as your SOCKS5 proxy in applications.

## Script Features

- Support for concurrent connections using threading
- Full SOCKS5 protocol implementation
- Error handling and proper connection closing
- Capability to run as a permanent service

## Important Notes

1. This script should be run on an intermediary server that has access to both the internet and the MTProto proxy.
2. For enhanced security, you can change SOCKS5_HOST to `0.0.0.0` to make it accessible from the local network.
3. If SOCKS5 authentication is required, you'll need to add the relevant code.

### 🔴 Attention
```
1. Limitations:
The MTProto protocol is specifically designed for Telegram communications. Therefore, if software such as web browsers or other general-purpose network applications connect to this SOCKS5 proxy, they will not be able to establish a successful connection. This is because only Telegram-related traffic is recognized and handled by MTProto. Unlike protocols such as Shadowsocks or VPNs, which can tunnel all system network traffic, this solution is limited solely to Telegram traffic.
2. Practical Use:
This script essentially serves as an intermediary between a Telegram client and an MTProto proxy. It allows clients such as Telegram Desktop to connect to a local SOCKS5 proxy, which in turn forwards the Telegram traffic through an MTProto proxy. This method is particularly useful for enabling access to Telegram in networks where direct connections may be restricted.
```

---

## 📧 Contact
- GitHub: [github.com/hesam-zahiri](https://github.com/hesam-zahiri)
