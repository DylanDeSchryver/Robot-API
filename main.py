from flask import Flask, request, jsonify
from adafruit_motorkit import MotorKit
import time

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <!-- initialize html-->
    
            <!DOCTYPE html>
        <html lang="en" dir="ltr">
          <head>
            <meta charset="utf-8">
            <title>Control Panel</title>
          </head>
          <style>
          <!-- CSS -->
          <!-- Aligns text-->
    h1
{text-align: center;}
h2
{text-align: center;}
h3
{text-align: center;}
button
{text-align: center;}
p
{text-align: center; font-size: large;}
 <!-- Sets background and text color-->
body
  {background-color:white;
     color: black;}
 <!-- Sets the default table color to white-->
table, th, td {
  border: 1px solid white;
  border-collapse: collapse;
}

h4{text-align: center;}




</style>
        <script>
        function send_command(direction) {
            fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'direction': direction })
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
                }
        </script>
          <script>
              var slider = document.getElementById("myRange");
var output = document.getElementById("demo");

          </script>


          <body>
          <!-- creates 2x2 table-->
<table style = "width:100%;border: 1px solid black;">
  <tr style = "height:700px;border: 1px solid black;">
  <!-- Row 1-->
      <!-- Box for the camra output-->
    <th style = "width:50%;border: 1px solid black;">camera</th>
    <!-- control panel-->
    <th style="border: 1px solid black;"><!-- 3x3 grid for control panel--><table style = "width:100%;">
    <!-- Row 1-->
  <tr style = "height:233px">
      <!-- Empty cell-->
    <th style = "width:33%"></th>
    <!-- Forward button-->
    <th style = "width:33%"><button style="height:218px;width:90%;font-size: 50px;" onclick="send_command('forward')" ><img src = "https://i.ibb.co/vmdwnbH/up-arrow-png-27157-1-removebg-preview.png" width="200" height="200"></button></th>
    <!-- Empty cell-->
    <th></th>
  </tr>
  <tr style = "height:233px">
  <!-- Row 2-->
      <!-- Left turn button-->
    <td><p><button style="height:217px;width:90%;font-size: 55px;" onclick="send_command('left')"><img src="https://i.ibb.co/bvkrDhz/image-2.png" width="200" height="200"></button></p></td>
    <!-- Stop and play button (in the same cell)-->
    <td><p><button style="height:217px;width:45%;font-size: 50px;" onclick="send_command('stop')"><img src="https://upload.wikimedia.org/wikipedia/commons/8/81/Stop_sign.png"  width="128" height="128"></button><button style="height:217px;width:45%;font-size: 50px;" onclick="send_command('play')"><img src="https://i.ibb.co/nzNB8WY/download-removebg-preview.png"  width="128" height="128"></button></p></td>
    <!-- Right turn button-->
    <td><p><button style="height:217px;width:90%;font-size: 55px;" onclick="send_command('right')"><img src = "https://i.ibb.co/C6D7hnz/image.png" width="200" height="200"></button></p></td>

  </tr>
  <tr style = "height:233px">
  <!-- Row 3-->
      <!-- Empty Cell-->
    <td></td>
    <!-- Move back button-->
    <td><p><button style="height:218px;width:90%;font-size: 50px;" onclick="send_command('backward')"><img src="https://i.ibb.co/6y7yBHR/image-1.png" width="200" height="200"></button></p></td>
    <!-- Empty cell-->    
    <td><p></p></td></table></th>
  </tr>
  <tr style = "height:700px;border: 1px solid black;">
    <!-- Row 2 of the big grid-->
    <!-- Where the line overaly should be-->
    <td style="border: 1px solid black;"><p>line</p></td>
    <!-- Wehere the log should be-->
    <td style="border: 1px solid black;"><p>log</p></td>
  </tr>

</table>
  </body>
        </html>
                        '''

# Create a dictionary to store the robot's current state eg. stopped
robot_state = "stopped"

# Initialize the MotorKit
kit = MotorKit(0x40)

# Define movement functions
def move_forward():
    kit.motor1.throttle = 0.77
    kit.motor2.throttle = 0.73
    robot_state = "moving forward"
def move_backward():
    kit.motor1.throttle = -0.80
    kit.motor2.throttle = -0.76
    robot_state = "moving backward"

def turn_left():
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = -0.75
    robot_state = "turning left"

def turn_right():
    kit.motor1.throttle = -0.76
    kit.motor2.throttle = 0.75
    robot_state = "turning right"

def stop_robot():
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    robot_state = "stopped"

def play_course():
  move_forward()
  time.sleep(4.1)
  stop_robot()
  time.sleep(1)
  turn_left()
  time.sleep(0.9)
  stop_robot()
  time.sleep(1)
  move_forward()
  time.sleep(2.4)
  stop_robot()
  time.sleep(1)
  move_backward()
  time.sleep(4.6)
  stop_robot()
  time.sleep(1)
  move_forward()
  time.sleep(2.5)
  stop_robot()
  time.sleep(1)
  turn_right()
  time.sleep(1.8)
  stop_robot()
  time.sleep(1)
  move_backward()
  time.sleep(5)
  stop_robot()
  time.sleep(1)
  move_forward()
  time.sleep(5)
  stop_robot()
  time.sleep(1)
  turn_right()
  time.sleep(0.9)
  stop_robot()
  time.sleep(1)
  move_forward()
  time.sleep(2.87)
  stop_robot()
  time.sleep(1)
  move_backward()
  time.sleep(4)
  stop_robot()
#endpoint to receive movement commands
@app.route('/move', methods=['POST'])
def move_robot():
    global robot_state
    data = request.get_json()
    direction = data.get('direction') #direction sent from send_command()
    # move robot based on the 'direction' received
    if direction == 'forward':
        move_forward()
    elif direction == 'backward':
        move_backward()
    elif direction == 'left':
        turn_left()
    elif direction == 'right':
        turn_right()
    elif direction == 'stop':
        stop_robot()
    elif direction == 'play':
      play_course()

    return jsonify({'message': f"Robot is now {robot_state}"}) #prints what state the robot is currently in.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #must be using 0.0.0.0 because this ensures that the server can be accessed from other computers.
#the default 127.0.0.1 doesnt allow other computers except the one running the server to process requests.
