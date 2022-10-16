def connect():
  print('Connecting to MQTT Broker...')
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  machine.reset()

try:
  client = connect()
except OSError as e:
  restart_and_reconnect()
  
push_button = Pin(2, Pin.IN)		#connect push button on pin2
push_button_Prv_state = False

while True:
  try:
    client.check_msg()
    logic_state = push_button.value()
    #print(logic_state)
    if logic_state == 1 and push_button_Prv_state == False:
          msg  = "ON"
          client.publish(topic_pub, msg)
          print('Publishing message: %s on topic %s' % (msg, topic_pub))
          push_button_Prv_state = True
    elif logic_state == 0 and push_button_Prv_state == True:
          msg  = "OFF"         
          client.publish(topic_pub, msg)
          print('Publishing message: %s on topic %s' % (msg, topic_pub))
          push_button_Prv_state = False
    time.sleep(1)
  except OSError as e:
    restart_and_reconnect()