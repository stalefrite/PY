#!/usr/bin/usr/python

import socket, os, sys, time, threading
from urllib.parse import urlparse

resolvers = [
    '8.8.8.8', # Google
    '9.9.9.9', # Quad9
    '1.1.1.1'  # Cloudflare
]

sub_domains = [
    'www', 'faq',  'login',  'landing',
    'app', 'info', 'about',  'contact',
    'cdn', 'home', 'forum',  'careers',
    'pay', 'news', 'signup', 'checkout',
    'sso', 'help', 'portal', 'community'
]

results = []

flag = threading.Event()

def probe(domain, timeout, delay):
    index = 0
    
    txid = None
    head = b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    tail = b"\x00\x01\x00\x01" # A (IPv4) Query
    
    delay   = float(delay) / 1000.0
    timeout = float(timeout) / 1000.0
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    
    for sub_domain in sub_domains:
        resolver = resolvers[index]
        
        # Transaction ID
        txid = os.urandom(2)
        
        sub_domain = sub_domain + "." + domain
        
        payload = b''
        for part in sub_domain.split('.'):
            if part:
                payload += bytes([len(part)]) + part.encode('utf-8')
                
        payload += b'\x00' # Terminal Byte
        
        query = txid + head + payload + tail
        
        try:
            s.sendto(query, (resolver, 53))
            
            data, _ = s.recvfrom(512)
            
            if len(data) < 12:
                print(f" [!] Malformed response from resolver {resolver}:53 --- Unable to probe: {sub_domain}")
            else:
                rcode = data[3] & 0x0F
            
                if rcode == 3:
                    # NXDOMAIN (0x83)
                    print(f" [-] Non-existent domain: {sub_domain}")
                elif rcode == 2:
                    # SERVFAIL (0x82)
                    print(f" [-] Resolver {resolver}:53 was unable to retrieve a response for {sub_domain}")
                elif rcode == 5:
                    # REFUSED (0x85)
                    print(f" [-] Request rejected along route. Unable to resolve {sub_domain}")
                elif rcode == 0:
                    # NOERROR (0x80)
                    print(f" ------> Active: {sub_domain}")
                else:
                    print(f" ------> Active: {sub_domain}")
        
        except socket.timeout:
            print(f" [-] Resolver {resolver} timed out. Unable to resolve {sub_domain}")
        except:
            print(f" [-] Error resolving {sub_domain} via {resolver}: {e}")
        
        index +=1
        
        if index > len(resolvers) - 1:
            index = 0
            
        if flag.is_set():
            break
            
        time.sleep(delay)
        
    s.close()

def get_content(file_path, flag: bool = False):
    content = []

    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        sys.exit("\r\n [-] Error! Invalid or missing file.\r\n")
                
    if os.path.getsize(file_path) == 0:
        sys.exit("\r\n [-] File is empty or missing!\r\n")
    
    try:
        with open(file_path, "r") as file_line:
            for line in file_line:
                line = line.replace(" ", "").strip().lstrip('./')
                
                if line:
                    content.append(line)
    except:
        sys.exit("\r\n [-] Critial error accessing file!\r\n")

    if flag:
        # DNS Resolvers
        global resolvers

        resolvers = content
    else:
        # Subdomains
        global sub_domains
        
        sub_domains = content

def main():
    pass

    print("""
                                                           .     
     :f:                             :;;;;;;;;;;;;;.       iWj.  
   ;D#E.            ,##############Wf.jWWWWWWWW###L         tE#G.
  i##;               ........jW##Wt           ,W#f           i##:
  i##:                     tW##Kt            ,##f            i##:
  i##:                   tW##E;             i##j             i##:
  i##:                 tW##E;              i##t              i##:
  i##:              .fW##D,               t##t               i##:
  i##:            .f###D,                t##i                j##:
  :G#Kt         .f####Gfffffffffff;     j##;               ,K#L: 
    .jW:       .fLLLLLLLLLLLLLLLLLi    :##,                ,t    
                                       ,W,                       
                                       ::                        
""")
    try:
        domain = input(" Domain to scan: ")
        
        domain = domain.lstrip("www.")
        
        choice = input(" Use custom resolvers? (Y/n): ")
        
        if choice.lower().startswith("y"):
            file_path = input(" Path (/tmp/rslvrs.txt): ")
            
            get_content(file_path, True)
            
        choice = input(" Use custom sub-domains? (Y/n): ")
        
        if choice.lower().startswith("y"):
            file_path = input(" Path (/tmp/names.txt): ")
        
            get_content(file_path, False)
        
        timeout = int(input(" Timeout (M/s) (Default = 1500): "))
        
        delay = int(input(" Delay (M/s) (Default = 50): "))
        
        input("\r\n Ready? Strike ENTER to scan and CTRL+C to abort...\r\n")
    except KeyboardInterrupt:
        sys.exit()
    except:
        sys.exit(" [-] Invalid value! Aborting...")
    
    try:
        job = threading.Thread(target=probe, args=(domain, timeout, delay))
        job.daemon = True
        job.start()

        job.join()
    except KeyboardInterrupt:
        flag.set()
    except Exception as e:
        print(e)
        
    sys.exit("\r\n Done.\r\n")

if __name__ == "__main__":
    main()
