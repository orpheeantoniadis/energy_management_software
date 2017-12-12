# -*- coding: utf-8 -*-
import socket,sys
from knxnet import *

from flask import Flask, jsonify, request

app = Flask(__name__)


IDs=[1,2,10,11]


udp_ip = "127.0.0.1"
udp_port = 3671


#### Standard route. Not to be used by students. Instead use next routes ####

@app.route("/cmd/<addr1>/<addr2>/<addr3>/<data>/<data_size>/<apci>")
def hello(addr1,addr2,addr3,data,data_size,apci):
	# sending a command
	addr=addr1+"/"+addr2+"/"+addr3
	dest_addr = knxnet.GroupAddress.from_str(addr)
	result    = send_data_to_group_addr(dest_addr, int(data), int(data_size), int(apci) )
	print(result)
	return jsonify(info=result)



#### Routes to be used by students ####

"""
@api {post} /v0/store/write Sends command to a store
@apiName command_store
@apiGroup Stores

@apiParam {Number} store_id Store ID
@apiParam {Number} value Wished value

@apiParamExample {json} Request-Exemple :
{
   'store_id' : '2',
   'value' : '200'
}

@apiSuccess {json} info Message confirming that the command was sent

@apiSuccessExample {json} Example of result in case of success:
{
   "info": "Command sent"
}

@apiDescription Sends write command to a specific store. Value should be between 0 and 255

"""

@app.route("/v0/store/write", methods=['GET', 'POST'],strict_slashes=False)
def store_write():
	if request.method=='POST':
		content = request.get_json()
		if all(item in content.keys() for item in ['store_id','value']):
			store_id = content['store_id']
			value = int(content['value'])
			# sending a command
			if (int(store_id) not in IDs):
				return jsonify(info="Wrong Store ID")
			if (value<0) or (value>255):
				return jsonify(info="Wrong value... Keep it between 0 and 255")
			addr="3/4/"+store_id
			dest_addr = knxnet.GroupAddress.from_str(addr)
			result    = send_data_to_group_addr(dest_addr, value, 2, 2 )
			print(result)
			return jsonify(info=result)
		return jsonify(info="Wrong input")
	return jsonify(info='use POST method')





"""
@api {get} /v0/store/read/<store_id> Reads Store's current value
@apiName read_store
@apiGroup Stores

@apiParam {Number} store_id Store ID

@apiSuccess {json} current_value current value

@apiSuccessExample {json} Example of result in case of success:
{
  "current_value": "150"
}

@apiDescription Reads value of a specific store

"""
@app.route("/v0/store/read/<store_id>")
def store_read(store_id):
	# sending a command
	if (int(store_id) not in IDs):
		return jsonify(info="Wrong Store ID")
	addr="4/4/"+store_id
	dest_addr = knxnet.GroupAddress.from_str(addr)
	result    = send_data_to_group_addr(dest_addr, 0, 2, 0)
	print(result)
	return jsonify(current_value=result)






"""
@api {post} /v0/radiator/write Sends command to a radiator
@apiName command_radiator
@apiGroup Radiators

@apiParam {Number} radiator_id Radiator ID
@apiParam {Number} value Wished value

@apiParamExample {json} Request-Exemple :
{
   'radiator_id' : '1',
   'value' : '200'
}

@apiSuccess {json} info Message confirming that the command was sent

@apiSuccessExample {json} Example of result in case of success:
{
   "info": "Command sent"
}

@apiDescription Sends write command to a specific radiator. Value should be between 0 and 255

"""
@app.route("/v0/radiator/write", methods=['GET', 'POST'],strict_slashes=False)
def radiator_write():
	if request.method=='POST':
		content = request.get_json()
		if all(item in content.keys() for item in ['radiator_id','value']):
			radiator_id = content['radiator_id']
			value = int(content['value'])
			# sending a command
			if (int(radiator_id) not in IDs):
				return jsonify(info="Wrong Radiator ID")
			if (value<0) or (value>255):
				return jsonify(info="Wrong value... Keep it between 0 and 255")
			addr="0/4/"+radiator_id
			dest_addr = knxnet.GroupAddress.from_str(addr)
			result    = send_data_to_group_addr(dest_addr, value, 2, 2 )
			print(result)
			return jsonify(info=result)
		return jsonify(info="Wrong input")
	return jsonify(info='use POST method')






"""
@api {get} /v0/radiator/read/<radiator_id> Reads Radiator's current value
@apiName read_radiator
@apiGroup Radiators

@apiParam {Number} radiator_id Radiator ID

@apiSuccess {json} current_value current value

@apiSuccessExample {json} Example of result in case of success:
{
  "current_value": "120"
}

@apiDescription Reads value of a specific radiator

"""
@app.route("/v0/radiator/read/<radiator_id>")
def radiator_read(radiator_id):
	# sending a command
	if (int(radiator_id) not in IDs):
		return jsonify(info="Wrong Radiator ID")
	addr="0/4/"+radiator_id
	dest_addr = knxnet.GroupAddress.from_str(addr)
	result    = send_data_to_group_addr(dest_addr, 0, 2, 0 )
	print(result)
	return jsonify(current_value=result)








def send_data_to_group_addr(dest_group_addr, data, data_size, apci ):
	data_endpoint = ('0.0.0.0', 0)
	control_enpoint = ('0.0.0.0', 0)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('',3672))


	# -> Connection request
	conn_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,
								   control_enpoint,
								   data_endpoint)
	sock.sendto(conn_req.frame, (udp_ip, udp_port))

	# <- Connection response
	data_recv, addr = sock.recvfrom(1024)
	conn_resp = knxnet.decode_frame(data_recv)
	print(conn_resp.status)

	if conn_resp.status == 0x0:
			# -> Connection state request
			conn_state_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,
												 conn_resp.channel_id,
												 control_enpoint)
			sock.sendto(conn_state_req.frame, (udp_ip, udp_port))

			# <- Connection state response
			data_recv, addr = sock.recvfrom(1024)
			conn_state_resp = knxnet.decode_frame(data_recv)
			print(conn_state_resp.status)

			if conn_state_resp.status == 0x0:
				# -> Tunnel request ##################
				tunnel_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
												 dest_group_addr,
												 conn_resp.channel_id,
												 data,
												 data_size,
												 apci)
				sock.sendto(tunnel_req.frame, (udp_ip, udp_port))

				# <- Tunnel ack
				data_recv, addr = sock.recvfrom(1024)
				ack = knxnet.decode_frame(data_recv)
				print(ack.status)

				if ack.status == 0x0:
					####### <- Tunnel Request
					data_recv, addr = sock.recvfrom(1024)
					tunnel_req_recv = knxnet.decode_frame(data_recv)

					####### -> Tunnel ack
					if tunnel_req_recv.data_service == 0x2e:
						status_error = 0x00
					else:
						status_error = 0x01
					tunnel_ack = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_ACK,
													 conn_resp.channel_id,
													 status_error,
													 tunnel_req_recv.sequence_counter)
					sock.sendto(tunnel_ack.frame, (udp_ip, udp_port))


					if apci == 0x0: # if apci == 0x0 then the command sent was a read command we get an extra Tunnel Request datagram containing the value

						####### <- Tunnel Request (Last Response from read)
						data_recv, addr = sock.recvfrom(1024)
						tunnel_req_recv_bis = knxnet.decode_frame(data_recv)


			# Disconnect request
			disconnect_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST,
												 conn_resp.channel_id,
												 control_enpoint)
			sock.sendto(disconnect_req.frame, (udp_ip, udp_port))

			# Disconnect response
			data_recv, addr = sock.recvfrom(1024)
			disconnect_resp = knxnet.decode_frame(data_recv)

	if apci == 0x0: # if the command sent was a read command we return the value else we return a confirmation message
		if tunnel_req_recv_bis is not None:
			return str(tunnel_req_recv_bis.data)
	elif ((tunnel_ack is not None) and (tunnel_ack.status == 0x0)):
		return 'Command sent'
	else:
		return 'Error'







if __name__ == "__main__":


    	app.run('0.0.0.0',port=5001)
	#addr      = '3/4/9' # store address
"""	data      = sys.argv[1]
	data_size = int(sys.argv[2])
	apci      = sys.argv[3]   # we put apci == 2 to write the data into the actuator, apci == 0 to read from it
	addr      = sys.argv[4]   # group address

	# sending a command
	dest_addr = knxnet.GroupAddress.from_str(addr)
	result    = send_data_to_group_addr(dest_addr, int(data), data_size, int(apci) )
	print(result)
"""
