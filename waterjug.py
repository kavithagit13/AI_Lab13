from queue import PriorityQueue

class State:
    def __init__(self, jugs):
        self.jugs = jugs

    def __eq__(self, other):
        return self.jugs == other.jugs

    def __hash__(self):
        return hash(str(self.jugs))

    def __str__(self):
        return str(self.jugs)

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.cost = 0

        if self.parent:
            self.cost = self.parent.cost + 1

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.state == other.state

def successors(state, capacities):
    successors = []
    for i in range(len(state.jugs)):
        for j in range(len(state.jugs)):
            if i != j:
                next_state = list(state.jugs)
                amount = min(state.jugs[i], capacities[j] - state.jugs[j])
                next_state[i] -= amount
                next_state[j] += amount
                successors.append(State(tuple(next_state)))
    return successors

def heuristic(state, target):
    return sum(abs(jug - goal) for jug, goal in zip(state.jugs, target))

def a_star(start, target, capacities):
    frontier = PriorityQueue()
    frontier.put(Node(start))
    explored = set()

    while not frontier.empty():
        current_node = frontier.get()
        current_state = current_node.state

        if current_state == target:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        explored.add(current_state)

        for successor_state in successors(current_state, capacities):
            successor_node = Node(successor_state, current_node)
            if successor_state not in explored:
                frontier.put(successor_node)

    return None

def main():
    capacities = (4, 3)  # Capacities of the jugs
    start_state = State((0, 0))  # Initial state of the jugs
    target_state = State((2, 0))  # Target state of the jugs

    path = a_star(start_state, target_state, capacities)

    if path:
        print("Solution Found:")
        for idx, state in enumerate(path):
            print(f"Step {idx}: {state}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
