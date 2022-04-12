# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from primerBot import Bot


click_thread = Bot()
click_thread.start()
pauseKey = KeyCode(char='a')	
stopKey = KeyCode.from_char('q')

# key as argument
def on_press(key):
    
  # start_stop_key will stop clicking
  # if running flag is set to true
    if key == pauseKey:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
              
    # here exit method is called and when
    # key is pressed it terminates auto clicker
    elif key == stopKey:
        click_thread.exit()
        listener.stop()

with Listener(on_press=on_press) as listener:
	listener.join()