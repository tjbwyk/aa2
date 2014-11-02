__author__ = 'fbuettner'
from policy import Policy
import random

class Player(object):
  """
  superclass for predator and prey
  implements common properties like position
  """
  def __init__(self, location=(0,0)):
    self.location = location
    self.field = None


  def set_policy(self, policy):
    self.policy = policy

  def act(self, seed=None):
    if(self.policy == None):
      print "No Policy set!"
      raise

    if seed != None:
      random.seed(seed)

    move = random.random()
    nextStates = self.policy.getNextStates()
    probability, state = nextStates.pop()

    while move > probability and len(nextStates) > 0:
      prob, state = nextStates.pop()
      probability += prob

    self.location = state
