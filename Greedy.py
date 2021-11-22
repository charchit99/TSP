import matplotlib.pyplot as plt

ALGO = 'GREEDY'
PAUSE_DURATION = 0.01


class Greedy:
    
    def make_path(self, plot = False, show_transitions = False):
        if plot:
            self.plot_city_points()
        
        while self.number_cities_left > 0:
            current_city = self.current_path[-1]
            best_index, next_city = min(enumerate(self.cities_left), key = lambda item: item[1].distance(current_city))
            del self.cities_left[best_index]
            self.current_path.append(next_city)
            self.number_cities_left -= 1
            if show_transitions:
                self.plot_transitions()
        self.number_cities_left -= 1
        self.current_path.append(self.current_path[0])
        if show_transitions:
            self.plot_transitions()
        
        return path_cost(self.current_path)
                
    
    def plot_transitions(self):
        x_begin, y_begin, x_end, y_end = self.current_path[-2].x, self.current_path[-2].y, self.current_path[-1].x, self.current_path[-1].y
        plt.plot([x_begin, x_end], [y_begin, y_end], 'ro')
        plt.plot([x_begin, x_end], [y_begin, y_end], 'g') 
        plt.draw()
        #plt.pause(PAUSE_DURATION)
        if self.number_cities_left == -1:
            plt.pause(100)
        else:
            plt.pause(PAUSE_DURATION)

    def plot_city_points(self):

        fig = plt.figure(0)
        #fig.title(ALGO)

        x_coordinates = [item.x for item in self.cities_left]
        x_coordinates.append(self.current_path[0].x)

        y_coordinates = [item.y for item in self.cities_left]
        y_coordinates.append(self.current_path[0].y)

        plt.plot(x_coordinates, y_coordinates, 'ro')
    
    def __init__(self, cities):
        index_swap = 0
        temp = cities[0]
        cities[0] = cities[index_swap]
        cities[index_swap] = temp
        self.cities_left = cities[1:]
        self.current_path = [cities[0]]
        self.number_cities_left = len(self.cities_left)
    

if __name__ == "__main__":
    cities = []
    greedy = Greedy(cities)
    print(greedy.make_path(plot = True, show_transitions = True))




