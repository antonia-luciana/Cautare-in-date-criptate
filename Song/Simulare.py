from ClientSong import ClientSong
from AdminSong import AdminSong


s = ClientSong("Client")
a = AdminSong("Admin")
#print len(s.enc(s.toBites("Pneumonoultramicroscopicsilicovolcanoconiosis")))

word = "Ana"
seed = "187"
#print "Verific", a.verify(s.enc(word, seed), s.simetric_enc(word), s.getKey(s.simetric_enc(word)).bin)

#s.sendFiles('Admin','exemplu1.txt','exemplu2.txt')
#c = s.enc("This", "Client//exemplu1.txt")
Xk = s.Trapdoor("the")

#a.getFiles("Client",Xk)

#print s.dec(s.enc("t", "Client//exemplu1.txt").hex, "Client//exemplu1.txt")
#print s.enc("a", "Client//exemplu1.txt").hex
s.Dec_file("exemplu1.txt")
