import heapq

class PuzzleState:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.goal_state = tuple([i * self.size + j for i in range(self.size) for j in range(self.size)])

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.board)

    def get_blank_position(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    return i, j

    def move(self, direction):
        i, j = self.get_blank_position()
        new_board = [row[:] for row in self.board]

        if direction == "up" and i > 0:
            new_board[i][j], new_board[i - 1][j] = new_board[i - 1][j], new_board[i][j]
        elif direction == "down" and i < self.size - 1:
            new_board[i][j], new_board[i + 1][j] = new_board[i + 1][j], new_board[i][j]
        elif direction == "left" and j > 0:
            new_board[i][j], new_board[i][j - 1] = new_board[i][j - 1], new_board[i][j]
        elif direction == "right" and j < self.size - 1:
            new_board[i][j], new_board[i][j + 1] = new_board[i][j + 1], new_board[i][j]

        return PuzzleState(new_board)

    def is_goal_state(self):
        return tuple([cell for row in self.board for cell in row]) == self.goal_state

    def manhattan_distance(self):
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    row = self.board[i][j] // self.size
                    col = self.board[i][j] % self.size
                    distance += abs(row - i) + abs(col - j)
        return distance

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.cost = 0
        if parent:
            self.cost = parent.cost + 1

    def __lt__(self, other):
        return self.cost + self.state.manhattan_distance() < other.cost + other.state.manhattan_distance()

def a_star(initial_state):
    frontier = []
    explored = set()
    heapq.heappush(frontier, Node(initial_state))

    while frontier:
        current_node = heapq.heappop(frontier)
        current_state = current_node.state

        if current_state.is_goal_state():
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        explored.add(current_state)

        for direction in ["up", "down", "left", "right"]:
            next_state = current_state.move(direction)
            if next_state not in explored:
                heapq.heappush(frontier, Node(next_state, current_node))

    return None

def main():
    # Define the initial state
    initial_state = PuzzleState([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

    # Solve the puzzle using A* search
    solution_path = a_star(initial_state)

    if solution_path:
        print("Solution Found:")
        for idx, state in enumerate(solution_path):
            print(f"Step {idx + 1}:")
            print(state)
            print()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
