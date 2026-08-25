import os
import psycopg2
import redis
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_HOST = os.environ.get('DB_HOST', '')
DB_NAME = os.environ.get('DB_NAME', '')
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
REDIS_HOST = os.environ.get('REDIS_HOST', '')

if ':' in DB_HOST:
    db_host_only, db_port_only = DB_HOST.split(':')
else:
    db_host_only, db_port_only = DB_HOST, 5432

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pg_status = "❌ Connection Failed"
        redis_status = "❌ Connection Failed"
        visitor_count = 0

        try:
            conn = psycopg2.connect(
                host=db_host_only,
                port=db_port_only,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=3
            )
            pg_status = f"✅ Connected Successfully to Database '{DB_NAME}'!"
            conn.close()
        except Exception as e:
            pg_status = f"❌ Failed: {str(e)}"

        try:
            r = redis.Redis(host=REDIS_HOST, port=6379, socket_timeout=3)
            r.incr('hits')
            visitor_count = r.get('hits').decode('utf-8')
            redis_status = f"✅ Connected Successfully! (Total Page Visits: {visitor_count})"
        except Exception as e:
            redis_status = f"❌ Failed: {str(e)}"

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_response = f"""
        <html>
            <head><title>DevOps End-to-End Test</title></head>
            <body style="font-family: Arial; text-align: center; padding-top: 50px;">
                <h1>🚀 Hello World from Docker, Jenkins & AWS Infrastructure!</h1>
                <hr style="width: 50%;">
                <h3>Database Connections Status:</h3>
                <p><strong>PostgreSQL RDS:</strong> {pg_status}</p>
                <p><strong>Redis Cluster:</strong> {redis_status}</p>
            </body>
        </html>
        """
        self.wfile.write(html_response.encode('utf-8'))

if __name__ == '__main__':
    print("Server starting on port 8000...")
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    server.serve_forever()