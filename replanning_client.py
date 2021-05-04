import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print('Msg: ' + message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
    #         ws.send("robot_at,r1,cell0")
    #         # ws.send("act_up,r1,cell0,cell1")
    #         #ws.send("Hello %d" % i)
    #     time.sleep(1)
    #     ws.close()
    #     print("thread terminating...")
    # thread.start_new_thread(run, ())

def start(address, port):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://" + address + ":" + str(port) + "/connect",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()

def send(event):
    ws.send(event)
