import math
import random
from matplotlib import pyplot as plt

IMAGE_NUMBER = '1'
INFINITY = 999999999.0
ANT_POPULATION = 30
ITERATIONS = 250
TOTAL_CITIES = 10
DISTANCE_LIMIT = 500
PHEREMONE_EFFECT = 1
ALPHA = 1
BETA = 3
RHO = 0.1

# For random cities
CITIES = [(random.uniform(0, DISTANCE_LIMIT), random.uniform(0, DISTANCE_LIMIT)) for i in range(TOTAL_CITIES)]



class TSP:

    class Ant:
        
        def get_Pij(self, city, heuristic_total):
            return math.pow(self.edges[self.tour[-1]][city].pheromone, ALPHA) * math.pow(heuristic_total/self.edges[self.tour[-1]][city].weight, BETA)
        
        def decide_cutoff(self, max, choice = 'probabilistic'):
            if choice == 'probabilistic':
                return random.uniform(0.0, max)
            else:
                return max/2.0
        
        def get_weight(self, cityA, cityB):
            return self.edges[cityA][cityB].weight
        
        def get_total_distance(self):
            total_distance = 0
            for unvisited_city in self.unvisited_cities:
                total_distance += self.get_weight(self.tour[-1], unvisited_city)
            return total_distance
        
        def get_decider(self, total_distance):
            decider = 0
            for unvisited_city in self.unvisited_cities:
                decider += self.get_Pij(unvisited_city, total_distance)
            return decider

        def get_next_city(self):

            total_distance = self.get_total_distance()
            decider = self.get_decider(total_distance)
            cutoff = self.decide_cutoff(decider)
            cur_sum = 0
            for unvisited_city in self.unvisited_cities:
                cur_sum += self.get_Pij(unvisited_city, total_distance)
                if cur_sum >= cutoff:
                    return unvisited_city

        def find_tour(self):
            self.tour = [random.randint(0, self.num_cities - 1)]
            self.unvisited_cities = {city for city in range(self.num_cities) if city != self.tour[0]}
            for i in range(self.num_cities - 1):
                self.tour.append(self.get_next_city())
                self.unvisited_cities.remove(self.tour[-1])
            return self.tour

        def get_distance(self):
            self.distance = 0.0
            for i in range(self.num_cities):
                self.distance += self.edges[self.tour[i]][self.tour[(i + 1) % self.num_cities]].weight
            return self.distance
        
        def __init__(self, num_cities, edges):
            self.edges, self.tour, self.num_cities, self.distance, self.unvisited_cities = edges, None, num_cities, 0.0, {}

    class Edge:
        def __init__(self, first_city, second_city, weight, initial_pheromone):
            self.first_city, self.second_city, self.weight, self.pheromone = first_city, second_city, weight, initial_pheromone

    def distance_between_cities(self, city_A, city_B):
        return math.sqrt(pow(city_A[0] - city_B[0], 2) + pow(city_A[1] - city_B[1], 2))
    
    def make_cities(self, initial_pheromone):
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    self.edges[i][j] = self.Edge(i, j, self.distance_between_cities(self.cities[i], self.cities[j]), initial_pheromone)

    def deposit_pheromone(self, tour, distance):
        pheromone_to_add = PHEREMONE_EFFECT / distance
        for i in range(self.num_cities):
            self.edges[tour[i]][tour[(i + 1) % self.num_cities]].pheromone += pheromone_to_add
    
    def iteration_update(self):
        # Reduce the pheremone levels after each iteration.
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    self.edges[i][j].pheromone *= (1.0 - RHO)

    def distance_update(self, tour, distance):
        # Update the global best if necessary.
        if distance < self.best_distance:
            self.best_tour, self.best_distance = tour, distance

    def ACS(self):
        for iteration in range(self.iterations):
            for ant in self.ants:
                ant_tour = ant.find_tour()
                ant_distance = ant.get_distance()
                self.deposit_pheromone(ant_tour, ant_distance)
                self.distance_update(ant_tour, ant_distance)
            self.iteration_update()
            self.results.append(self.best_distance)
            

    def ELITIST(self):
        for iteration in range(self.iterations):
            for ant in self.ants:
                ant_tour = ant.find_tour()
                ant_distance = ant.get_distance()
                self.deposit_pheromone(ant_tour, ant_distance)
                self.distance_update(ant_tour, ant_distance)
            self.deposit_pheromone(self.best_tour, self.best_distance)
            self.iteration_update()
            self.results.append(self.best_distance)


    def display_summary(self):
        print("The trip sequence that the salesman should take following the", self.mode,"approach looks like:")
        for i in self.best_tour:
            print(i, '-> ', end = "")
        print(self.best_tour[0])
        print("Total distance =", self.best_distance, "\n")

    def run(self):
        if self.mode == 'ACS':
            self.ACS()
        else:
            self.ELITIST()
        self.display_summary()

    def plot(self):
        x, y = [], []
        for i in self.best_tour:
            x.append(self.cities[i][0])
            y.append(self.cities[i][1])
        x.append(x[0])
        y.append(y[0])

        plt.title(self.mode)
        plt.scatter(x, y)
        plt.plot(x, y, linewidth = 1)
        plt.show()
        scale = [i for i in range(1, self.iterations + 1)]
        plt.plot(scale, self.results)
        plt.show()
    
    def __init__(self, mode, iterations = 10, cities = None, ant_population = 5, initial_pheromone = 1.0):

        self.cities, self.num_cities, self.iterations, self.mode = cities, len(cities), iterations, mode
        self.edges = [[None] * self.num_cities for i in range(self.num_cities)]
        self.ant_population = ant_population
        self.best_distance, self.best_tour, self.results = INFINITY, [], []

        self.make_cities(initial_pheromone)
        self.ants = [self.Ant(self.num_cities, self.edges) for i in range(self.ant_population)]


if __name__ == "__main__":
    acs_instance = TSP(mode = "ACS", iterations = ITERATIONS, cities = CITIES, ant_population = ANT_POPULATION)
    acs_instance.run()
    acs_instance.plot()
    elitist_instance = TSP(mode = "Elitist", iterations = ITERATIONS, cities = CITIES, ant_population = ANT_POPULATION)
    elitist_instance.run()
    elitist_instance.plot()

