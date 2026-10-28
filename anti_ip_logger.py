import sys
import socket
import requests

def tor_check():
    try:
        with socket.create_connection(('127.0.0.1', 9050), timeout=3):
            print("[+] TOR service is active!")
            return True
    except:
        return False

def main():
    print("[~] Confirming TOR service is running...")
    if not tor_check():
        sys.exit("\r\n\t[-] Error: TOR service not running/available!\r\n")

    ua = logger = None

    try:
        logger = input("\r\nLink to suspected IP logger:\r\n")

        ua = input("\r\nCustom message to send:\r\n")
    except KeyboardInterrupt:
        sys.exit("[!] Aborted")
    except:
        sys.exit()

    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    headers = {
        'User-Agent': ua
    }

    session = requests.Session()
    session.proxies.update(proxies)
    session.headers.update(headers)

    try:
        print("\r\n[~] Sending request...")
        url = logger

        response = session.get(url, timeout=20)
        print("[+] Message delivered to endpoint!")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    # pip install requests[socks]
    main()
