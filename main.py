from field import Field
from predator import Predator
from prey import Prey
from policy import Policy

def main():
    # create field and characters
    environment = Field()
    cat = Predator()
    cat.set_policy(Policy(0.0, 0.25, 0.25, 0.25, 0.25))
    squirrel = Prey()
    squirrel.set_policy(Policy(0.8, 0.05, 0.05, 0.05, 0.05))
    # run simulation
    return None

if __name__ == '__main__':
    main()