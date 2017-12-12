cd doc/actuasim_iot
python3 actuasim.py &
cd ../../
cd doc/Actuator\ Server/
python3 KNX_REST_Server.py &
cd ../../
cd src/python
python REST_server.py &
python client.py &
cd ../nodejs
node server.js &
