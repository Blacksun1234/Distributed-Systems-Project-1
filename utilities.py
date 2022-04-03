def extra_data(data):
    data = data.split(" ")
    event = data[0]
    sender_id = data[1]
    timestamp = data[2]

    return event, sender_id, timestamp    

def build_data(event, node_id, timestamp, ):
    data = str(event) + " " + str(node_id) + " " + str(timestamp)
    return data
