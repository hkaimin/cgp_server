export LD_LIBRARY_PATH=/usr/local/python2.7/lib:/usr/local/libevent/lib:/usr/local/libgo/lib:$LD_LIBRARY_PATH
chmod +x ./gameserver
./gameserver main.py game start