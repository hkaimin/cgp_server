gcc -c ../engine/engine/ultrabson/*.c  -I/usr/local/python2.7/include/python2.7  -lpython2.7  -L/usr/local/python2.7/lib/ 
g++ ../engine/engine/main.cpp ../engine/engine/log/*.cpp ../engine/engine/misc/*.cpp *.o  -I/usr/local/python2.7/include/python2.7 -I/usr/local/libevent/include -I/usr/local/libgo/include -lpython2.7  -lpthread -levent -lgo -L/usr/local/python2.7/lib/ -L/usr/local/libgo/lib/ -L/usr/local/libevent/lib/ -o gameserver
rm -rf *.o
