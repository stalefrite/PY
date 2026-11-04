import sys, os, requests, re, time, threading
from bs4 import BeautifulSoup

tid   = None
board = None

flag = threading.Event()

def sort_links(extracted):
    ftypes = [
        '.webm','.png','.jpg','.jpeg','.gif','.mp4'
    ]
    
    to_download = []
      
    for link in extracted:
        for ftype in ftypes:
            if link.lower().endswith(ftype):
                new_link = link
                
                if new_link.startswith("//"):
                    new_link = '/' + new_link[2:]
                elif not new_link.startswith("/"):
                    new_link = '/' + new_link
                    
                new_link = 'https:/' + new_link
                
                to_download.append(new_link)
    
    to_download = list(set(to_download))
    return to_download

def get_links(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')

        new_links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        return new_links
    except Exception as e:
        sys.exit(f'\r\n\tError: {e}\r\n')

def get_html():
    url = f"https://boards.4chan.org/{board}/thread/{tid}"

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        else:
            sys.exit('\r\n [!]Alert: Thread is dead or banned.\r\n')
    except Exception as e:
        sys.exit(f'\r\n\tError: {e}\r\n')

def rip(passes, wait, html, dump):
    previous = []
    
    passed = 0

    while True:
        if passes > 0 and passed >= passes:
            break
        elif flag.is_set():
            break

        if passes != 0:
            print(f"\r\n [!] Pass: {passed + 1}/{passes}\r\n")
        else:
            print(f"\r\n [!] Pass: {passed + 1}/∞\r\n")
        
        print(' [~] Scraping HTML...')
        content = get_html()
        
        print(' [~] Extracting resource links...')
        new_links = get_links(content)

        print(' [~] Discarding external resources...')
        resources = sort_links(new_links)
        
        if previous:
            print(' [!] Checking for new resources...')
            resources = [link for link in resources if link not in previous]
        
        if not resources:
            print(" [!] No media detected! Ignoring pass...")
        else:
            print(' [~] Now downloading!\r\n')
        
            for resource in resources:
                try:
                    filename = os.path.basename(resource)
                    
                    filepath = os.path.join(dump, filename)
                    
                    response = requests.get(resource)
                    
                    if response.status_code == 200:
                        print(f" -----> Downloading: {resource}")
                        
                        if os.path.exists(filepath):
                            os.remove(filepath)
                            
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                            f.close()
                        
                        time.sleep(0.01)
                    else:
                        print(f" -----> Unable to download: {resource}")
                except Except as e:
                    print(f"\tError: {e}")

        if html.lower().startswith("y"):
            html_content = f"https://boards.4chan.org/{board}/thread/{tid}"
            
            html_path = os.path.join(dump, 'thread.html')
            
            try:
                response = requests.get(html_content)
                
                if os.path.exists(html_path):
                    os.remove(html_path)
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                    f.close()
            except:
                pass
                
        if not previous:
            previous = resources
        
        if passes == 0 or passed < passes - 1:
            print(f"\r\n [~] Sleeping for {wait} seconds...")
            time.sleep(wait)
            
        passed += 1

def link_check(url):
    global tid, board
    
    pattern = r"^https://boards\.4chan\.org/([^/]+)/thread/(\d+)"
    match = re.match(pattern, url)
    
    if not match:
        sys.exit("\r\n\tError! Invalid URL\r\n")
        
    board = match.group(1)
    tid   = match.group(2)
    
def main():

    print('''
       .::   .,-:::::   ::   .:   :::.   :::.    :::.      
     ,;';; ,;;;'````'  ,;;   ;;,  ;;`;;  `;;;;,  `;;;      
    ,[' [[ [[[        ,[[[,,,[[[ ,[[ '[[,  [[[[[. '[[      
    $P__$$c$$$        "$$$"""$$$c$$$cc$$$c $$$ "Y$c$$      
    `"""88"`88bo,__,o, 888   "88o888   888,888    Y88      
        MM   "YUMMMMMP"MMM    YMMYMM   ""` MMM     YM      
        
 :::::::..   :::::::::::::.::::::::::. .,:::::: :::::::..   
 ;;;;``;;;;  ;;; `;;;```.;;;`;;;```.;;;;;;;```` ;;;;``;;;;  
  [[[,/[[[`  [[[  `]]nnn]]`  `]]nnn]]`  [[cccc   [[[,/[[[`  
  $$$$$$c    $$$   $$$""      $$$""     $$""""   $$$$$$c    
  888b "88bo,888   888o       888o      888oo,__ 888b "88bo,
  MMMM   "W" MMM   YMMMb      YMMMb     """"YUMMMMMMM   "W" 
''')

    try:
        url = link_check(input(" Link to thread: "))
        
        passes = int(input(" Pass Count (0=infinite): "))
        
        wait = 0
        
        if passes != 1:
            wait = int(input(" Delay (sec) between passes (120=default): "))
            
        html = input(" Include ripped HTML layout? (Y/n): ")
        
        dump = input(" Download Path (ex- /tmp/): ")
        
        if not os.path.isdir(dump):
            sys.exit("\r\n\tPath does not exist.\r\n")

        input("\r\n Ready? Strike ENTER to rip and CTRL+C to end...\r\n")
    except KeyboardInterrupt:
        sys.exit("\r\b\tAborted.\r\n")
    except Exception as e:
        sys.exit(f"\r\n\tError: {e}\r\n")
    
    try:
        th = threading.Thread(target=rip, args=(passes, wait, html, dump))
        th.daemon = True
        th.start()
        
        th.join()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(e)
        
    flag.set()
    time.sleep(0.001)
    
    print("\r\nDone.\r\n")    
        
if __name__ == "__main__":
    main()
