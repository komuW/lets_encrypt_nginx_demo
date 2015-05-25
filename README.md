# A demo of setting up https for nginx


# pre-requisites
*  [vagrant](https://www.vagrantup.com)

# Usage
* git clone this repository
* cd to the project directory
* vagrant up
* visit [https:localhost:8700](https:localhost:8700)

# Tutorial:

#### HTTPS #####
- HTTPS ("HTTP over TLS", "HTTP over SSL", or "HTTP Secure") is a communications protocol for secure communication over a computer network.       
- Technically, it is not a protocol in and of itself; simply layering HTTP on top of the SSL or TLS protocol, thus adding the security capabilities of SSL/TLS.        
- HTTPS provides authentication of the website/web-server that one is communicating with, protectin against man-in-the-middle attacks.        
- Additionally, it provides bidirectional encryption of communications, protectin against eavesdropping and tampering with the contents of the communication.         
- SSL is suited HTTP since it can provide some protection even if only one side of the communication is authenticated, where typically only the server is authenticated (by the client examining the server's certificate).         
- Web browsers know how to trust HTTPS websites based on certificate authorities that come pre-installed in their software. Certificate authorities, such as Symantec, Comodo, GeoTrust, are in this way being trusted by web browser creators to provide valid certificates.          
- A site must be completely hosted over HTTPS, without having some of its contents loaded over HTTP, or the user will be vulnerable to some attacks and surveillance.           
- SSL comes in two options, simple and mutual. The mutual one requires the client to also install a personal certificate into their client/browser in order to authenticate themselves        

# server setup          
- To prepare a web server to accept HTTPS connections, u must create a public key certificate for the web server.         
- This cert must be signed by a trusted CA for clients(browsers) to accept it without warning. The CA certifies that the cert holder is the operator of the web server that presents it.           
- Browsers are distributed with a list of signing certificates of major CA's so that they can verify certificates signed by them.

# acquiring certs 
- costs between 1k - 10k per year.          
- CAcert.org        
- https://letsencrypt.org/        
    `$ sudo apt-get install lets-encrypt`          
    `$ lets-encrypt www.example.com`

# ssl handshake
- A client requests access to a protected resource.        
- Server presents its certificate to the client.        
- Client verifies the server's certificate.     
  - If successful:          
      -the client sends its certificate to the server.          
    else:           
      -user is warned of problem & informed that an encrypted and authenticated connection cannot be established         
  - Server verifies the client's credentials.         
- If successful, the server grants access to the protected resource requested by the client.           

# Web Server Configurations:

# a good resource when configuring https:
https://wiki.mozilla.org/Security/Server_Side_TLS       
    `""" The goal of this document is to help operational teams with the configuration of TLS on servers. 
        All Mozilla sites and deployment should follow the recommendations below.
    """ - https://wiki.mozilla.org/Security/Server_Side_TLS`        

- There are 3 recommended configurations:         
           Configuration and its Oldest compatible client:           
  - Modern                - Firefox 27, Chrome 22, IE 11, Opera 14, Safari 7, Android 4.4, Java 8        
  - Intermediate          - Firefox 1, Chrome 1, IE 7, Opera 5, Safari 1, Windows XP IE8, Android 2.3, Java 7 (mostly WinXP)        
  - Old                   - Windows XP IE6, Java 6             

- The ordering of a ciphersuite is very important because it decides which algorithms are going to be selected in priority. The recommendation above prioritizes algorithms that provide perfect forward secrecy.          
- The concept of forward secrecy is simple: client and server negotiate a key that never hits the wire, and is destroyed at the end of the session.         
- With Forward Secrecy, if an attacker gets a hold of the server's private key, it will not be able to decrypt past communications.          
- Session Resumption is the ability to reuse the session secrets previously negotiated between a client and a server for a new TLS connection. This feature greatly increases the speed establishment of TLS connections after the first handshake, and is very useful for connections that use Perfect Forward Secrecy with a slow handshake like DHE.           
- OCSP Stapling - When connecting to a server, clients should verify the validity of the server certificate using either a Certificate Revocation List (CRL), or an Online Certificate Status Protocol (OCSP) record. side effect is that OCSP requests must be made to a 3rd party OCSP responder when connecting to a server, which adds latency and potential failures. solution is to allow the server to send its cached OCSP record during the TLS handshake, therefore bypassing the OCSP responder, this saves a roundtrip.         
- HSTS is a HTTP header sent by a server to a client, indicating that the current site must only be accessed over HTTPS until expiration of the HSTS value is reached.          
- SSL stripping(type of downgrade attack) is a man-in-the-middle attack in which a network attacker prevents a client(web-browser) from upgrading to an SSL connection in a subtle way that would likely go unnoticed by a user.          
- HTTP Strict Transport Security (HSTS) is a web security policy mechanism which is necessary to protect secure HTTPS websites against downgrade attacks. It allows web servers to declare that web browsers (clientts) should only interact with it using secure HTTPS connections, and never via HTTP protocol.            
- The HSTS Policy is communicated by the server to the user agent via a HTTP response header field named "Strict-Transport-Security"
  -When a web app/server issues HSTS Policy to clients, conformant clients behave as follows:           
     - Auto turn any insecure links referencing the web app into secure links.          
     - If the security of the connection cannot be ensured, show an error message and do not allow the user to access the web application           
    
# different webserver config generator:
  `- https://mozilla.github.io/server-side-tls/ssl-config-generator/`

# generate cert
- check if ua nginx version supports tls          
`$ nginx -V`
  `.... TLS SNI support enabled ....`           

# How to create certificate.             
     NB: dont run any of this commands in a vagrant env(do it locally.)
1. Generate a key that will be later used to generate the CSR cert          
`$ sudo openssl genrsa -des3 -out server.key 2048`              
  u'll be asked for a passphrase, ideally atleast 8chars (by default it accepts 4chars and above)         

next, generate the key without a passphrase(to help in running nginx in daemon)           
`$ sudo openssl rsa -in server.key -out server.key.insecure `              
then, rename the keys             
`$ sudo mv server.key server.key.secure`            
`$ sudo mv server.key.insecure server.key`        

2. create the CSR            
`$ sudo openssl req -new -key server.key -out server.csr `            
  u'll be prompted for passphrase             
  then other prompts follow, important one is one requesting for Common Name/server FQDN/YOUR name: enter domain name (or ip address)         

3. You can now submit this CSR(server.csr) file to a CA for processing. The CA will use this CSR file and issue the certificate
 Alternatively; u can create self-signed certificate using this CSR.                

4. create a self-signed cert
`$ sudo openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt`              
 u'll be prompted for passphrase         
 
5. Installing the Certificate           
You can install the key file server.key and certificate file server.crt, or the certificate file issued by your CA, by running following commands at a terminal prompt:         
`$ sudo cp server.crt /etc/ssl/certs`
`$ sudo cp server.key /etc/ssl/private`            
- then configure ua webserver(nginx etc)             
`"""
    u can also create the SSL key and certificate files in one command:             
    `$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt`

    - req: specifies that we want to use X.509 certificate signing request (CSR) management            
    - -x509: modify prev subcommand, sayin we want to make a self-signed certificate instead of generating a certificate signing request                   
    - -nodes: This tells OpenSSL to skip the option to secure our certificate with a passphrase         
    - -days 365: validity in days           
    - -newkey rsa:2048: we want to generate a new certificate and a new key at the same time.
        We did not create the key that is required to sign the certificate in a previous step          
    - keyout: location where to place generated key           
    - -out: This tells OpenSSL where to place the certificate that we are creating.            

    - the command above will issue u with prompts which u r supposed to respond to
         The most important one is one requesting Common Name (e.g. server FQDN or YOUR name): enter ua domain name here (or IP address)            

    - configure nginx            
        ssl_certificate /etc/nginx/ssl/nginx.crt;           
        ssl_certificate_key /etc/nginx/ssl/nginx.key;            
    `$ sudo service nginx restart`
"""`