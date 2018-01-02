
Functionality:

1. Parse the connections from the 40000 port (openvpn management port)
2. Ping the clients to check if there are any routing issues.
3. Update iptables route for new connection.
4. Update esc_tbl (Table) in SqlDB for new connection entry data and port number in
   ESC_DEPLOY_INFO db.
5. Fork a new thread for new client along with 15sec timer.
6. Rest server 


Process:
#1, #2 and #6 

Thread:
#5


Queues:
 Q1 is the Queue that is shared between two process #1 and #2
 new/modify/del connection #1 -> Q1 <- #2 (Ping)

 Q2 is the Queue for the comm link UP/Down status from #2

----------------------------------------------------------- 
process functionality:

#1 - P1

Create Q1, Q2, Q3(Heart Beat), Q4(Ping)

Create a thread to parse connection from openvpn server manager. (X1)

a. Parse connection
b. Update client list (new/modify/del)
c. Update iptables
d. Update SQLDB
e. Post connection information to Queue Q1

f. Create a thread for every new incoming connection (Openvpn client) (C1, C2,
C3, ... n)
g. Q2 thread blocks for data and update the SQLDB (X2)
h. Q3 thread blocks for data and feed the data into #f

#2 (Ping ) - P2

a. Read data from Q1
b. Ping connections and update the comm link in SQLDB.

#3 - (Rest server) - P3

a. Fetches the data from Flask API and post to Q3.
b. HB fails - raise a trap and post information to Q2.




