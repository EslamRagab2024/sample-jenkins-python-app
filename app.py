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

        # 1. PostgreSQL Check
        if db_host_only:
            try:
                conn = psycopg2.connect(
                    host=db_host_only,
                    port=db_port_only,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    connect_timeout=2
                )
                pg_status = f"✅ Connected Successfully to '{DB_NAME}'!"
                conn.close()
            except Exception as e:
                pg_status = f"❌ Failed: {str(e)}"

        # 2. Redis Check
        if REDIS_HOST:
            try:
                r = redis.Redis(host=REDIS_HOST, port=6379, socket_timeout=2)
                r.incr('hits')
                visitor_count = r.get('hits').decode('utf-8')
                redis_status = f"✅ Connected Successfully! Visits: {visitor_count}"
            except Exception as e:
                redis_status = f"❌ Failed: {str(e)}"

        # 3. Always Return 200 OK Response
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_response = f"""
            <html>
                <body>
                    <h1>🚀 App Status</h1>
                    <p>PostgreSQL: {pg_status}</p>
                    <p>Redis: {redis_status}</p>
                </body>
            </html>
            """
            self.wfile.write(html_response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling request: {e}")

if __name__ == '__main__':
    print("Server starting on port 8000...")
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    server.serve_forever()