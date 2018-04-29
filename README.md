# Code-Collaboration-Tool
run `python /user1/.multhread_server` to start server
run `python /user{1/2/3/4} to start client`

`autocopy.py` is used to copy all files in user1 to user2/3/4 except "server_files"

files that starts with should be placed in `user1/server_files`

current issues:
PORT hard coded in file
no exception changed

suggested to do in future:
MD5 check
create a _bak file at /files when start to avoid some error
