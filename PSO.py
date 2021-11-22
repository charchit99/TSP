import random
import math
import matplotlib.pyplot as plt

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

#Function to read input data
def read_cities(size):
    cities = []
    with open(f'test_data/cities_{size}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    return cities

#Function to generate random cities/nodes
def generate_cities(size):
    return [City(x=int(random.random()*1000), y=int(random.random()*1000)) for _ in range(size)]

#Total cost for salesman to travel across all cities
def path_cost(route):
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])

#This denotes a particle within a global set or one configuration of route in many available routes.
class Particle:
    def __init__(self, route, cost=None):
        self.current_route = route
        self.pbest = route
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()

    def update_pbest_and_cost(self):
        self.current_cost = self.path_cost()
        if self.pbest_cost > self.current_cost:
            self.pbest_cost = self.current_cost
            self.pbest = self.current_route

    def path_cost(self):
        return path_cost(self.current_route)

#Build a random route
def random_route(cities):
    return random.sample(cities, len(cities))

#Build a greedy route
def greedy_route(cities, start_index):
    not_visited = cities[:]
    del not_visited[start_index]
    route = [cities[start_index]]
    while len(not_visited):
        index, nearest_city = min(enumerate(not_visited), key=lambda item: item[1].distance(route[-1]))
        route.append(nearest_city)
        del not_visited[index]
    return route

#Function to start with some configurations: some random and some greedy
def initial_config(cities, num_cities, population_size):
    random_populatn = [random_route(cities) for _ in range(population_size - 1)]
    greedy_populatn = [greedy_route(cities,i) for i in range(int(num_cities/10))]
    return [*random_populatn, *greedy_populatn]

#PSO algorithm
def PSO(iterations, population_size, num_cities, gbest_prob=1.0, complement_pbest_prob=1.0, cities=None):
    gbest = None
    gcost_iter = []
    particles = []

    #Initialise configs
    solutions = initial_config(cities, num_cities, population_size)
    
    #Define initial costs and routes
    particles = [Particle(route=solution) for solution in solutions]

    #Initialise gbest
    gbest = min(particles, key=lambda p: p.pbest_cost)
    print(f"Initial path cost is {gbest.pbest_cost}")
    plt.ion()
    plt.draw()
    for t in range(iterations):
        #Global best is the best configuration among different particle configs till now
        gbest = min(particles, key=lambda p: p.pbest_cost)

        #In every 20 iters
        if t % 20 == 0:
            plt.figure(0)
            plt.plot(gcost_iter, 'g')
            plt.ylabel('Total Distance')
            plt.xlabel('Generations')
            fig = plt.figure(0)
            fig.suptitle('PSO path cost')
            
            x_list, y_list = [], []
            for city in gbest.pbest:
                x_list.append(city.x)
                y_list.append(city.y)
            x_list.append(gbest.pbest[0].x)
            y_list.append(gbest.pbest[0].y)

            fig = plt.figure(1)
            fig.clear()
            fig.suptitle(f'PSO iteration: {t}')
            plt.plot(x_list, y_list, 'ro')
            plt.plot(x_list, y_list, 'g')
            plt.draw()
            plt.pause(.001)

        #Path cost for this iteration
        gcost_iter.append(gbest.pbest_cost)

        for particle in particles:
            temp_velocity = []
            temp_gbest = gbest.pbest[:]
            this_iter_route = particle.current_route[:]

            #For each config, try changing it to pbest for that particular config
            for i in range(len(cities)):
                if this_iter_route[i] != particle.pbest[i]:
                    swap = (i, particle.pbest.index(this_iter_route[i]), complement_pbest_prob)
                    temp_velocity.append(swap)
                    tmp1 = this_iter_route[swap[0]]
                    tmp2 = this_iter_route[swap[1]] 
                    this_iter_route[swap[0]] = tmp2
                    this_iter_route[swap[1]] = tmp1

            #For each config, try changing it to global best among all configs
            for i in range(len(cities)):
                if this_iter_route[i] != temp_gbest[i]:
                    swap = (i, temp_gbest.index(this_iter_route[i]), gbest_prob)
                    temp_velocity.append(swap)
                    temp_gbest[swap[0]], temp_gbest[swap[1]] = temp_gbest[swap[1]], temp_gbest[swap[0]]

            #Swap according to probabilities
            for swap in temp_velocity:
                if random.random() < swap[2]:
                    tmp1 = this_iter_route[swap[0]]
                    tmp2 = this_iter_route[swap[1]] 
                    this_iter_route[swap[0]] = tmp2
                    this_iter_route[swap[1]] = tmp1

            #Update route
            particle.current_route = this_iter_route
            #Update pbest for config
            particle.update_pbest_and_cost()

    return gbest
        
if __name__ == "__main__":
    num_cities = 51
    #Read input cities
    cities = read_cities(num_cities)
    
    #Run PSO algo
    gbest = PSO(iterations=1500, population_size=num_cities*5, num_cities=num_cities, complement_pbest_prob=0.15, gbest_prob=0.02, cities=cities)
    
    #Print final values
    print(f'Final path cost: {gbest.pbest_cost}\nFinal route: {gbest.pbest}')

    #Plot final route
    x_list, y_list = [], []
    for city in gbest.pbest:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(gbest.pbest[0].x)
    y_list.append(gbest.pbest[0].y)
    
    fig = plt.figure(1)
    fig.suptitle('PSO final route')

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list)
    plt.show(block=True)

