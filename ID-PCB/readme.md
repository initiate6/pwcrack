Name: IRC distributed password cracking bot. ID-PCB

Client Side: Files you need to excute client. 

setup.py: 

* Check to see if python 2.7 is installed. # TODO
* gather info on computer. OS type and version, 32bit/64bit, how many cores, how much memory, Video cards, driver versions. 
* create client ID. 
* Save information to file for client.py
* If something is wrong notify how to fix it. 
* Check to see if hashcat is located on computer if not download what is required based on computer. # TODO
* #TODO get info on osx.
* Ask user for e-mail address so we can get a hold of them if the client drops off.


client.py:

* Connect to IRC server and give clientID, state, system info.
* Wait for command to excute. Verify command is for hashcat program and excute. 
* update server with HashCat stats every 5mins and post to its personal irc channel.
* Once command has completed successfully upload found file to SecureFTP site.  

Async_subprocess.py:

* Allows you to use process.communicate() asynchronously. 
* Added poll() to get returncode.

winmem.py:
* Used for windows PC to get RAM info. 
* #TODO There is a better way to handle this just need to switch it over. 
 

Server Side: Files you need to excute on server.
rserver.py:

* Creates a pwcrack.db sqlite3 database. With the following tables: clients, algorithms, completed, 
* Connect to IRC server. 
* Keeps a up to date database of all the clients connected with their ClientID, state, system info

InitalBrute.py:

* Command & Control server for the inital bruteforce. 
* Update script with how many clients you want to work on it and at what power level.
* Goes through hashes = [ 'raw-md5', 'raw-sha1', 'raw-md4', 'mysql-sha1', 'ntlm', 'nsldap', 'raw-md5u' ]
* Brute force full keyspace for 1-7 char.
* Change script and re-run for password length 8char. Change Markov Threshold to limit keyspace. 
* Change script and re-run for password length 9char. Change Markov Threshold to limit keyspace even further. 
 

algorithmTable.py:

* creates a database algorithm.db with Algorithm type 'raw-md5', HashFile Location 'hashes/raw-md5.hash', HashCat M code '-m 0', GPUOptions for AMD and NV. -n 256 -u 1024
* #TODO add hash types and GPU options. 



sqlite3 database: 

* File name pwcrack.db
* Tables: Clients 
          * Client ID, State, system, bits, threads, gpuType, Auth, e-mail.

* File name algorithm.db
* Tables: Clients 
          * algorithm, HashFile, mcode, AMDaccel, AMDloops, NVaccel, NVloops

* File name BFTable.db
* Tables: hashType+bftable 
          * start, charset, status

