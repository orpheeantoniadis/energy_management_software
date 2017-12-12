ps -e | grep "python REST_server.py" | grep -v grep | awk '{print $1}' | xargs kill
ps -e | grep "python client.py" | grep -v grep | awk '{print $1}' | xargs kill
# Python 3
ps -e | grep "Python actuasim.py" | grep -v grep | awk '{print $1}' | xargs kill
ps -e | grep "Python KNX_REST_Server.py" | grep -v grep | awk '{print $1}' | xargs kill

killall node -SIGINT
