import sys
import re
import requests
import ssl
import socket
from datetime import datetime


def get_certificate_chain(url):
    parsed_url = requests.utils.urlparse(url)
    hostname = parsed_url.hostname
    port = (
        parsed_url.port
        if parsed_url.port
        else (443 if parsed_url.scheme == "https" else 80)
    )

    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert(True)
            pem_cert = ssl.DER_cert_to_PEM_cert(cert)
            return pem_cert


def write_header_file(cert, filename):
    with open(filename + ".pem", "w") as f:
        f.write(cert)

    with open(filename + ".h", "w") as f:
        f.write(
            f"// Generated using https://github.com/xyzshantaram/root-ca-downloader at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n"
        )
        f.write(f"const char *{filename.upper()}_CERT = \n")
        for line in cert.splitlines():
            f.write(f'"{line}\\n"\n')
        f.write(";\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    output_filename = re.sub(r"^https?://", "", url).replace(".", "_")

    cert = get_certificate_chain(url)
    write_header_file(cert, output_filename)
    print(f"Certificate files written to {output_filename}.h and {output_filename}.pem")


if __name__ == "__main__":
    main()
