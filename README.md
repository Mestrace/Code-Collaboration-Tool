# Code-Collaboration-Tool
run `python multithread_server.py` in /user1 to start server
run `python m_client.py` in user1/2/3/4 to start client and type the username

`autocopy.py` is used to copy all files in user1 to user2/3/4 except "server_files". This is for development, you may not need to use it.

files that starts with should be placed in `user1/server_files`
each user should make changes in `user*/files` thus will be able to `PUSH*` it
Currently the file works with `test.py` which is hard coded in `multithread_server.py`. If you want to work with other files, change the `FILENAME` variable in line 17


NOTE:
To quit the program, enter `QUIT` in chatting, don't close it directly thus will cause fatal error to the program. 
PORT hard coded in file
no exception handled

suggested to do in future:
MD5 check
No duplicate user name are allowed
