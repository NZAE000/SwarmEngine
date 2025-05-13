import math
from pathlib import Path
from scipy.special import gamma
import random as rnd
import numpy as np
import sys

sys.path.append(str(Path(__file__).parent.parent))
from engine.swarm import Swarm
from engine.agent import Agent


##########################################################################
# WO ALGORITHM:
# Inspired from the behaviors of walrus in migrating, breeding,
# roosting and foraging, a new metaheuristic
# algorithm, WO, for the first time. Two assumptions need to be
# clarified here:
#   (1) Walrus populations judge population behavior by danger and
#   safety signals.
#   (2) Behavioral and role divisions in walrus populations are modeled
#   in the walrus algorithm. Specifically, the walrus algorithm assumes
#   social structures and interactions between male, female,
#   and juvenile walruses.
##########################################################################
class WO(Swarm):
    def __init__(self, problem, iterations, nAgents):
        super().__init__("WO", problem, iterations, nAgents)

    # Variable params for each iteration.
        self.danger_signal = 0
        self.safety_signal = 0
        self.A_dng_factor  = 0
        self.R_dng_factor  = 0
        self.alfa = 0 # α decreases from 1 first to 0 with the number of iterations t, and T is the maximum iteration.
        self.beta = 0
        self.vigilant1    = Agent(self.problem.dimension)
        self.vigilant2    = Agent(self.problem.dimension)
        self.current_male = Agent(self.problem.dimension)
        self.n_teen    = 0
        self.n_adult   = 0
        self.n_male    = 0
        self.n_female  = 0
        self.teens_w   = []
        self.females_w = []
        self.males_w   = []
        self.lmda = 3/2
        self.stdX = math.pow(self.factorial(1+self.lmda) * math.sin(math.pi*self.lmda/2) / (self.factorial((1+self.lmda)/2) * self.lmda * math.pow(2, (self.lmda-1)/1)), 1/self.lmda)
        self.stdY = 1

        self.move = self.moveBasedMigration # Default callable.

    #def chooseMovement(self):
    #    
    #    if self.danger_signal >= 1: # Exploration phase.
    #        # Update new position of each walrus.
    #        print()
    #    else: # Exploitation phase.
    #        #if ()

    ## Exploration.
    def moveBasedMigration(self, walrus, motion_log):
        for j in range(self.problem.dimension):
            migration_step = (self.vigilant1.position[j] - self.vigilant2.position[j]) * self.beta * math.pow(rnd.random(), 2)
            next_pos = walrus.position[j] + migration_step
            walrus.position[j] = self.normalize(next_pos, j)
            motion_log.append(next_pos)

    # In the quasi-Monte Carlo method, the Halton sequence is a widely used method to generate randomly distributed sequences.
    def halton_index(self, index, base):
        result = 0.0
        f = 1.0 / base
        i = index
        while i > 0:
            result += f * (i % base)
            i //= base
            f /= base
        return result
    
    def generate_first_n_primes(self, n):
        primes = []
        num = 2
        while len(primes) < n:
            is_prime = all(num % p != 0 for p in primes)
            if is_prime:
                primes.append(num)
            num += 1
        return primes

    # Adopting Halton sequence distribution for male walrus position update can allow a broader distribution of the population with search space
    def moveMalesWalrus(self, male_w, motion_log):
        bases = self.generate_first_n_primes(self.problem.dimension)
        for j in range(self.problem.dimension):
            lower_bound = self.problem.minDomain(j)
            upper_bound = self.problem.maxDomain(j)
            halton      = self.halton_index(j+1, bases[j])
            next_pos    = lower_bound + halton * (upper_bound - lower_bound)
            male_w.position[j] = self.normalize(next_pos, j)
            motion_log.append(next_pos)
    
    # The female walrus is influenced by male walrus (Malet i,j) and the lead walrus (Xtbest). As the process of iteration, the female walrus is gradually influenced less by the mate and more by the leader.
    def moveFemalesWalrus(self, female_w, motion_log):
        for j in range(self.problem.dimension):
            next_pos = female_w.position[j] + self.alfa * (self.current_male.position[j] - female_w.position[j]) + (1 - self.alfa) * (self.gBest.position[j] - female_w.position[j])
            female_w.position[j] = self.normalize(next_pos, j)
            motion_log.append(next_pos)

    def normal_distr(self, mean, std):
        return np.random.normal(mean, std, 1)[0]
    
    def factorial(self, x):
        """
        Calculate the factorial of a decimal number using the Gamma function.
        Args:
            x: The decimal number.
        Returns:
            The factorial of x.
        """
        return gamma(x + 1)
    
    def levyFlight(self):
        return 0.05 * (self.normal_distr(0, self.stdX) / math.pow(abs(self.normal_distr(0, self.stdY)), 1/self.lmda))

    # Juvenile walruses at the edge of the population are often targeted by killer whales and polar bears. Therefore, juvenile walruses need to update their current position to avoid predation.
    def moveTeenWalrus(self, teen_w, motion_log):
        for j in range(self.problem.dimension):
            levy          = self.levyFlight()
            safety_pos    = self.gBest.position[j] + teen_w.position[j] * levy
            distress_coef = rnd.random() # Distress coefficient of juvenile walrus.
            next_pos      = (safety_pos - teen_w.position[j]) * distress_coef
            teen_w.position[j] = self.normalize(next_pos, j)
            motion_log.append(next_pos)

    # Walruses are also attacked by natural predators during underwater foraging, and they will flee from their current activity area based on danger signals from their peers.
    def moveFleeing(self, walrus, motion_log):
        for j in range(self.problem.dimension):
            next_pos = walrus.position[j] * self.R_dng_factor - abs(self.gBest.position[j] - walrus.position[j]) * math.pow(rnd.random(), 2) # self.gBest.position[j] - walrus.position[j] denotes the distance between the current walrus and the best walrus.
            walrus.position[j] = self.normalize(next_pos, j)
            motion_log.append(next_pos)

    # Walruses can cooperate to forage and move according to the location of other walruses in the population and sharing location information can help the whole walrus herd to find the sea area with higher food abundance.
    def moveGathering(self, walrus, motion_log):
        for j in range(self.problem.dimension):
            a1 = self.beta * rnd.random() - self.beta
            a2 = self.beta * rnd.random() - self.beta
            b1 = math.tan(rnd.uniform(0, math.pi))
            b2 = math.tan(rnd.uniform(0, math.pi))
            X1 = self.gBest.position[j] - a1 * b1 * abs(self.gBest.position[j] - walrus.position[j])
            X2 = self.swarm[1].position[j] - a2 * b2 * abs(self.swarm[1].position[j] - walrus.position[j])
            next_pos = (X1 + X2) / 2
            print("X1:", X1, "X2:", X2)
            walrus.position[j] = self.normalize(next_pos, j)
            motion_log.append(next_pos)

# IMPLEMENTS! #########################################################

# INIT ALL
    def initAllAgents(self):
        # Clear all walruses.
        self.teens_w.clear()
        self.females_w.clear()
        self.males_w.clear()

        self.n_teen   = int(0.10 * self.nAgents)         # 10% population.
        self.n_adult  = self.nAgents - self.n_teen       # 90% population.
        self.n_female = self.n_male = self.n_adult // 2  # 45% each.

        # Create lists with references (without copies) to swarm agents.
        self.teens_w   = self.swarm[:self.n_teen]
        self.females_w = self.swarm[self.n_teen:self.n_teen + self.n_female]
        self.males_w   = self.swarm[self.n_teen + self.n_female:self.n_teen + self.n_female + self.n_male]

# UPDATE ALL
    def updateAgents(self):
        #print("\niter: ", super().currentIter)
        #print("aca")
        if abs(self.danger_signal) >= 1: # Exploration phase.
            print("aca1")
            # Update new position of each walrus.
            # Choose vigilantes randomly and set beta.
            self.vigilant1 = self.swarm[rnd.randint(0, self.nAgents-1)]
            self.vigilant2 = self.swarm[rnd.randint(0, self.nAgents-1)]
            self.beta = 1 - 1 / ( 1 + math.exp( -(self.currentIter - (self.maxIter/2)) / self.maxIter) * 10 )
            self.move = self.moveBasedMigration
            for walrus in self.swarm:
                self.updateOne(walrus)
                #print("after  => pos: ", agent.position, " best_pos: ", agent.pBest, "\n")
        else: # Exploitation phase.
            if self.safety_signal >= 0.5: # (1) Roosting behavior: The male, female and juvenile walruses are our classification of population members. They have different ways of renewing their position.
                print("aca2")
                # Step 1: Redistribution of male walruses.
                self.move = self.moveMalesWalrus
                for male_w in self.males_w:
                    self.updateOne(male_w)
                print("aca3")
                # Step 2: Position update of female walruses.
                self.move = self.moveFemalesWalrus
                for i in range(self.n_female):
                    self.current_male = self.males_w[i]
                    self.updateOne(self.females_w[i])
                print("aca4")
                # Step 3: Position update of juvenile walruses.
                self.move = self.moveTeenWalrus
                for teen_w in self.teens_w:
                    self.updateOne(teen_w)

            else: # (2) Foraging behavior: Underwater foraging includes fleeing and gathering behaviors.
                if abs(self.danger_signal) >= 0.5: # Fleeing behavior.
                    print("aca5")
                    self.move = self.moveFleeing
                    for walrus in self.swarm:
                        self.updateOne(walrus)

                else: # Gathering behavior.
                    print("aca6")
                    self.move = self.moveGathering
                    self.beta = 1 - 1 / ( 1 + math.exp( -(self.currentIter - (self.maxIter/2)) / self.maxIter) * 10 )
                    for walrus in self.swarm:
                        self.updateOne(walrus)


# MOVE ONE
    def moveAgent(self, agent, motion_log):
        self.move(agent, motion_log)

# UPDATE PARAMETERS
    def updateParams(self):
        self.alfa          = 1 - (self.currentIter / self.maxIter)
        self.A_dng_factor  = 2 * self.alfa
        self.R_dng_factor  = 2 * (rnd.random() - 1)
        self.danger_signal = self.A_dng_factor * self.R_dng_factor
        self.safety_signal = rnd.random()
        #self.move = self.chooseMovement()

