def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    import os
    import http.server
    import socketserver
    
    print("Simple Calculator")
    print(f"2 + 3 = {add(2, 3)}")
    
    # Keep the process alive for Render by starting a dummy web server
    PORT = int(os.environ.get("PORT", 8000))
    Handler = http.server.SimpleHTTPRequestHandler
    
    print(f"Starting dummy server on port {PORT} to keep Render happy...")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
