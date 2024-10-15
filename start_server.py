import argparse
import requests
import hashlib
import os
import shutil
from http.server import SimpleHTTPRequestHandler, HTTPServer

def _download_repo(repo_url, pat):
    headers = {
        "Authorization": f"token {pat}"
    }
    
    # Download the compressed file
    response = requests.get(repo_url, headers=headers)
    
    if response.status_code == 200:
        temp_filename = "temp"
        with open(temp_filename, 'wb') as temp_file:
            temp_file.write(response.content)
        print(f"Downloaded {temp_filename}")
        return temp_filename
    else:
        print(f"Failed to download the repository: {response.status_code}")
        exit(1)

def _calc_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def _rename_file(original_filename, sha256_value):
    os.rename(original_filename, sha256_value)
    print(f"Renamed file to {sha256_value}")
    return sha256_value

def download_and_prepare_repo(repo_urls, pat, web_server_base):
    for repo in repo_urls:
        compressed_filename = _download_repo(repo, pat)
        sha256_value = _calc_sha256(compressed_filename)
        hashed_filename = _rename_file(compressed_filename, sha256_value)
        destination_path = os.path.join(web_server_base, hashed_filename)
        shutil.move(hashed_filename, destination_path)

def start_web_server(web_server_base, port):
    class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            return super().do_GET()

    os.chdir(web_server_base)
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    print(f"Serving at http://localhost:{port}/")
    httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-urls', type=str, nargs='+', required=True, help="The URIs of the repositories to download,")
    parser.add_argument('--port', type=int, required=True, help="The port to serve the webserver on.")
    parser.add_argument('--pat', type=str, required=True, help="Your personal access token for authentication.")

    args = parser.parse_args()

    web_server_base = "web_server_base"
    os.makedirs(web_server_base, exist_ok=True)

    download_and_prepare_repo(args.repo_urls, args.pat, web_server_base)
    
    start_web_server(web_server_base, args.port)

if __name__ == "__main__":
    main()