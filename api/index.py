from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib.parse import parse_qs, urlparse

BEARER_TOKEN = "a2i0k-00exk3iVQ-G-5R4yE-TSvAdzp-D2YP-jG_RTskx8h-fU6hUAR6P8BpOS-6"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        phone_number = query.get('num', [None])[0]
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if not phone_number:
            response = json.dumps({
                "status": "error",
                "message": "Please provide a num parameter. Example: /api?num=8274930574"
            })
            self.wfile.write(response.encode())
            return
        
        # Truecaller API call
        url = "https://search5-noneu.truecaller.com/v2/search"
        params = {
            'q': phone_number,
            'countryCode': 'IN',
            'type': '4',
            'encoding': 'json'
        }
        headers = {
            'User-Agent': 'Truecaller/26.19.7 (Android;15)',
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }
        
        try:
            api_response = requests.get(url, params=params, headers=headers)
            
            if api_response.status_code == 200:
                data = api_response.json()
                self.wfile.write(json.dumps(data, indent=2).encode())
            else:
                error_response = {
                    "status": "error",
                    "code": api_response.status_code,
                    "message": "API request failed"
                }
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())
