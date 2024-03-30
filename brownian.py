import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os


class Environment(object):
    def __init__(self, width):
      self.width =width
      
      
class Robot(object):
    def __init__(self, x, space_env, radius,  v_speed = 1.0, w_speed = math.pi/8):

      self.state=x

      #direction is in radians
      self.dir = 0
      self.v_speed = v_speed

      #angular speed is in radians/step
      self.w_speed = w_speed
      self.env = space_env
      self.radius = radius

    def step(self):
      new_state = self.state + self.v_speed * np.array([np.cos(self.dir),np.sin(self.dir)])

      collision=False
      if new_state[0]>self.env.width-self.radius or new_state[0]<self.radius or new_state[1]>self.env.width-self.radius or new_state[1]<self.radius:
        self.dir = -self.dir
        collision=True

      if collision:
        duration = random.randint(2, 10)
        for i in range(duration):
          self.dir += self.w_speed
      
      self.state[0] = min(max(new_state[0],self.radius),self.env.width-self.radius)
      self.state[1] = min(max(new_state[1],self.radius),self.env.width-self.radius)

def create_robot(square_width=20,robot_radius=1):
  if robot_radius>square_width/4:
    print("Not enough space, overwriting... ")
    square_width=20
    robot_radius=1

  x0=np.array([square_width/2, square_width/2])
  space_env = Environment(square_width)
  robot = Robot(x0, space_env, robot_radius)
  return robot


def visualize(robot,N=30):
  images = []
  name='brownian'
  
  for i in range(N):
      robot.step()
      #print(robot.state[0], robot.state[1])
      plt.figure(figsize=(14, 11))
      circle1=plt.Circle((robot.state[0], robot.state[1]), robot.radius, color='g')
      plt.gca().add_patch(circle1)
      plt.arrow(robot.state[0], robot.state[1], robot.radius*math.cos(robot.dir), robot.radius*math.sin(robot.dir), head_width=0.15, color='k', length_includes_head=True)
      plt.ylim(0, robot.env.width)
      plt.xlim(0, robot.env.width)

      fname = f'./{name}_{i}.png'
      plt.savefig(fname)
      plt.close()
      images.append(imageio.imread(fname))
      os.remove(fname)

  fname = f'./{name}.gif'
  imageio.mimsave(fname, images,format='GIF', fps = N / 20)
  print("Done. ")