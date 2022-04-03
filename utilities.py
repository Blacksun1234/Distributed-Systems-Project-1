def extra_data(data):
    data = data.split(" ")
    event = data[0]
    sender_id = data[1]
    timestamp = data[2]
    port = data[3]

    return event, sender_id, timestamp,port   

def build_data(event, node_id, timestamp, port):
    data = str(event) + " " + str(node_id) + " " + str(timestamp) + " " + str(port)
    return data
