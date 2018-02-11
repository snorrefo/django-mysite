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


def websockets(request):
    template_name = 'chartjs/websockets.html'
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
        client.subscribe("happy-bubbles/presence/ha/#")

    # The callback for when a PUBLISH message is received from the server.

    def on_message_esp_link_03(client, userdata, msg):
        client.msgs["esp-link-03-r3"].nmessages += 1
        client.msgs["esp-link-03-r3"].msg = msg
        print("esp-link-03-r3: received message")

    def on_message_esp_link_04(client, userdata, msg):
        client.msgs["esp-link-04-g4"].nmessages += 1
        client.msgs["esp-link-04-g4"].msg = msg
        print("esp-link-04-g4: received message")

    client = mqtt.Client()

    class Test(object):
        def __init__(self):
            self.msg = None
            self.nmessages = 0

    # msgs = {"esp-link-03-r3": Test()}
    msgs = {"esp-link-03-r3": Test(), "esp-link-04-g4": Test()}
    client.msgs = msgs

    client.on_connect = on_connect

    client.message_callback_add("happy-bubbles/presence/ha/esp-link-03-r3",
                                on_message_esp_link_03)

    client.message_callback_add("happy-bubbles/presence/ha/esp-link-04-g4",
                                on_message_esp_link_04)

    # happy-bubbles/presence/ha/esp-link-03-r3
    # {"id":"58b0f5296168","name":"iPhone","distance":45}

    client.connect("10.0.0.40", 1883, 2)

    while time.perf_counter() - t0 < 4:
        n = 0
        for key, msg in client.msgs.items():
            if client.msgs[key].nmessages > 0:
                n += 1
        # print(n)
        if n == len(client.msgs):
            # All topics have received 1 or more messages
            print("All topics have received 1 or more messages")
            break

        client.loop()

    print(time.perf_counter())

    client.disconnect()

    i = 1
    x = []
    y = []
    for key, msg in client.msgs.items():
        if client.msgs[key].nmessages > 0:
            print("message:")
            payload = client.msgs[key].msg.payload
            print(payload)
            msg = json.loads(payload)
            x.append(i)
            y.append(msg['distance'])
            print(x)
            print(y)

        else:
            print("no message:")
            x.append(i)
            y.append(-1)
            print(x)
            print(y)

        i += 1

    # if client.msgs["esp-link-03-r3"].nmessages > 0:
    #     print("message:")
    #     payload = client.msgs["esp-link-03-r3"].msg.payload
    #     print(payload)
    #     msg = json.loads(payload)
    #     x = 3
    #     y = msg['distance']
    #     print(x)
    #     print(y)
    # else:
    #     print("no message")
    #     x = 3
    #     y = -1
    #     print(x)
    #     print(y)

    return {'x': x, 'y': y}
