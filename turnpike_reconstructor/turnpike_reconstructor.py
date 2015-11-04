from collections import defaultdict, namedtuple
from math import sqrt, ceil
from enum import Enum
    
Candidate = namedtuple('Candidate', 'side point distances')

class Sides(Enum):
    left = 0
    right = 1

class Distances():
    def __init__(self, vector):
        self.vector = vector
        self.dictionary = defaultdict(int)
        for distance in self.vector:
            self.dictionary[distance] += 1
        self.largest_distance = self.max()

    def max(self):
        return max(self.vector)
    
    def possible_points(self):
        return set(range(self.largest_distance))
    
    def num_points(self):
        sq_rt = sqrt(len(self.vector) * 2)
        num_points = ceil(sq_rt)
        return int(num_points)
    
    def __getitem__(self, key):
        return self.dictionary[key]
    
    def __sub__(self, distance):
        self.vector.remove(distance)
        self.dictionary[distance] -= 1
        return self
        
    def __add__(self, distance):
        self.vector.append(distance)
        self.dictionary[distance] += 1
        return self
    
    def __contains__(self, distance):
        return self.dictionary[distance] >= 1
    
    def __str__(self):
        return ("Distances:\n    vector representation: {}\n    dictionary representation: {}".format(self.vector, self.dictionary))
        
class Points():
    def __init__(self, distances):
        num_points = distances.num_points()
        self.vector = [None] * num_points
        self.left_pointer = 0
        self.right_pointer = num_points - 1
        self.set_point(Candidate(Sides.left, 0, None))
        self.set_point(Candidate(Sides.right, distances.largest_distance, None))
        distances -= distances.largest_distance
        
    def set_point(self, candidate):
        if candidate.side == Sides.left:
            self.vector[self.left_pointer] = candidate.point
            self.left_pointer += 1
        elif candidate.side == Sides.right:
            self.vector[self.right_pointer] = candidate.point
            self.right_pointer -= 1
        
    def unset_point(self, candidate):
        if candidate.side == Sides.left:
            self.left_pointer -= 1
            self.vector[self.left_pointer] = None
        elif candidate.side == Sides.right:
            self.right_pointer += 1
            self.vector[self.right_pointer] = None
        
    def get_distances(self, proposed_point):
        distances = []
        for point in self.vector:
            if point is not None:
                distances.append(abs(proposed_point-point))
        return distances
    
    def __str__(self):
        return str(self.vector)

class TurnpikeReconstructor():
    def __init__(self, distance_vector):
        self.distances = Distances(distance_vector)
        self.points = Points(self.distances)
        self.possible_points = self.distances.possible_points()
        self.backtrack()
        
    def backtrack(self):
        if self.is_solution():
            self.process_solution()
            self.finished = True
        else:
            candidates = self.get_candidates()
            for candidate in candidates:
                self.make_move(candidate)
                self.backtrack()
                self.unmake_move(candidate)
    
    def make_move(self, candidate):
        for distance in candidate.distances:
            self.distances -= distance
        self.points.set_point(candidate)
        self.possible_points.remove(candidate.point)
           
    def unmake_move(self, candidate):
        self.points.unset_point(candidate)
        self.possible_points.add(candidate.point)
        for distance in candidate.distances:
            self.distances += distance
    
    def get_candidates(self):
        candidates = []
        distance = self.distances.max()
        for i, p in enumerate([distance, self.distances.largest_distance - distance]):
            rel_distances = self.points.get_distances(p)
            if p in self.possible_points and all([rel_distances.count(distance) <= self.distances[distance] for distance in set(rel_distances)]):
                side = Sides.right if i == 0 else Sides.left
                c = Candidate(side, p, rel_distances)
                candidates.append(c)
        return candidates
    
    def is_solution(self):
        if self.points.left_pointer > self.points.right_pointer:
            return True
        else:
            return False
        
    def process_solution(self):
        print (self.points)
        
        
if __name__ == "__main__":
    distances = [1,2,2,2,3,3,3,4,5,5,5,6,7,8,10]
    tp = TurnpikeReconstructor(distances)
    
    distances2 = [1,1,2,2,6,7,8,8,9,10]
    tp2 = TurnpikeReconstructor(distances2)
    
    distances3 = [11,10,9,8,7,6,6,5,5,4,3,2,2,1,1]
    tp3 = TurnpikeReconstructor(distances3)
    
    