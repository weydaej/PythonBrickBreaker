# PythonBrickBreaker

Breakout, otherwise known as brick breaker, developed in python with the pygame library. 

I began with a 500x500 window and created three separate classes: Ball, Paddle and Brick. Each class has init, 
update and draw methods. I gave each object a set of properties such as size and position, and animate the ball 
and paddle by applying velocity to each. I wrote a collision method that implements physics and calculates which 
angles the ball should bounce according to the angles at which it interacts with the paddle, bricks and edges of
the window. For the main method, my while loop implements the update and draw functions I use to continuously call 
the ball and paddle and reposition them in real time at 60 frames per second.
