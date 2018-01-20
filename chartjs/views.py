from django.http import HttpResponse
from django.shortcuts import render
# https://pypi.python.org/pypi/djangoajax
from django_ajax.decorators import ajax
import paho.mqtt.client as mqtt
import time
import json


def index(request):
    template_name = 'chartjs/index.html'
    context = {}
    return render(request, template_name, context)


# def api_pos(request):
#     return HttpResponse("Test.")
@ajax
def api_pos(request):

    t0 = time.perf_counter()
    print(t0)
    # The callback for when the client receives a CONNACK response from
    # the server.

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("happy-bubbles/ble/esp-link-03-r3/raw/170393f4dd7a")
        client.subscribe("testsfw")

    # The callback for when a PUBLISH message is received from the server.


    def on_message(client, userdata, msg):
        # try:
        # print(type(msg.payload))
        # print("{} {}".format(msg.topic, msg.payload))
        client.nmessages += 1
        client.lastmsg = msg
        print("received message")



        # return {'x': msg.topic, 'y': msg.payload}

    client = mqtt.Client()
    client.nmessages = 0
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("10.0.0.40", 1883, 2)

    while time.perf_counter() - t0 < 4:
        if client.nmessages > 0:
            break
        client.loop()

    print(time.perf_counter())

    client.disconnect()

    if client.nmessages > 0:
        print("message:")
        print(client.lastmsg.payload)
        msg = json.loads(client.lastmsg.payload)
        x = msg['x']
        y = msg['y']
        print(x)
        print(y)
    else:
        print("no message")
        x = -1
        y = -1

    return {'x': x, 'y': y}
