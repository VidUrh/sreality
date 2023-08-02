from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.flats import FlatsSpider

from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            flats = self.fetch_flats()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>500 FLATS FROM SREALITY</h1>")
            self.wfile.write(f"""<p>Found {len(flats)} flats</p>
                             <table><tr><th>Title</th><th>Image</th></tr>
                             """.encode())
            for flat in flats:
                self.wfile.write(f"<tr><td><h2>{flat[1]}</h2></td>".encode())
                self.wfile.write(f'<td><img src="{flat[2]}"></td></tr>'.encode())
            self.wfile.write(b"</table></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

    def fetch_flats(self):
        conn = psycopg2.connect(
            dbname="sreality",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flats LIMIT 500")
        flats = cursor.fetchall()
        cursor.close()
        conn.close()
        return flats

def run_server():
    host_name = "0.0.0.0"
    port_number = 8080
    httpd = HTTPServer((host_name, port_number), HTTPRequestHandler)
    print(f"Server started on http://{host_name}:{port_number}")
    httpd.serve_forever()

if __name__ == "__main__":
        
    process = CrawlerProcess(get_project_settings())
    process.crawl(FlatsSpider)
    process.start()
    run_server()