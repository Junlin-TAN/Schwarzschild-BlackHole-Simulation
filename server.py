import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"服务器已启动，正在监听端口 {PORT}")
    print(f"请在浏览器中打开以下链接： http://localhost:{PORT}")
    httpd.serve_forever()