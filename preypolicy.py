
class PreyPolicy(Policy):
  """
    implementation of the policy of the prey
  """
	
  fixedActions = [(0.8, (0, 0))]
  flexActions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

  def updatePolicy(field, agent):
    """
      updates the probabilities of the states
    """
     
   newStates = []

    probability = 1
    for fixed in fixedActions:
      prob, action = fixed
      probability -= prob

	
    for flex in flexActions:
      newStates.append(field.get_new_coordinates(agent.position, flex))  	

    for agent in field.getPredators():
      if agent.__class__.__name__==Predator.__name__:
        newStates.remove(agent.location)

    flexProb = probabilty / len(newStates)  

    allStates = [ (flexProb, x) for x in newStates ]
    allStates.extend(fixedActions)

    return allStates
