Name: IRC distributed password cracking bot. ID-PCB

Client Side:

setup.py: 

* Check to see if python 2.7 is installed. # TODO
* gather info on computer. OS type and version, 32bit/64bit, how many cores, how much memory, Video cards, driver versions. 
* create client ID. 
* Save information to file for client.py
* If something is wrong notify how to fix it. 
* Check to see if hashcat is located on computer if not download what is required based on computer. # TODO
* #TODO get info on linux and osx.
* #TODO ask user for e-mail address so we can get a hold of them if the client drops off.


client.py:

* Connect to IRC server and give clientID, state, system info.
* Wait for command to excute. Verify command is for hashcat program and excute. 
* update server with HashCat stats every 5mins and post to its personal irc channel.



rserver.py:

* Creates a pwcrack.db sqlite3 database. With the following tables: clients, algorithms, completed, 
* Connect to IRC server. 
* Keeps a up to date database of all the clients connected with their ClientID, state, system info

ccserver.py:

* Command & Control server.
* Two types of commands. Brute force and rule based for GPU
* Two types of commands. Brute force and rule based for CPU
* Loads the pwcrack.db creates different commands for the clients to excute based on how many clients are ready and system info.


sqlite3 database: 

* File name pwcrack.db
* Tables:

List tables and keys with value types. #TODO 