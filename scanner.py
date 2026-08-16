import urllib.request

url = input("Enter website URL: ")

response = urllib.request.urlopen(url)

security_headers = {
    "Strict-Transport-Security": "Forces HTTPS",
    "Content-Security-Policy": "Controls browser resources",
    "X-Content-Type-Options": "Prevents MIME sniffing",
    "X-Frame-Options": "Helps prevent clickjacking"
}

print("\nHTTP Status:", response.status)
print("\nSecurity Header Scan")
print("-" * 30)

found = 0

for header, purpose in security_headers.items():
    if header in response.headers:
        print("[+] " + header + " : FOUND")
        found += 1
    else:
        print("[-] " + header + " : MISSING")

print("\nScore:", found, "/", len(security_headers))