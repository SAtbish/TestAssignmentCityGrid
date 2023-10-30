from random import randint
import matplotlib.pyplot as plt


class CityGrid:
    """
    A class representing a grid for a city layout with towers.

    Attributes:
        n (int): Number of rows in the grid.
        m (int): Number of columns in the grid.
        tower_radius (int): The range of coverage for each tower.
        grid (list[list[int|str]]): A 2D grid representing the city layout.
        towers (list[tuple[int, int]]): List of tower coordinates.
    """

    def __init__(self, n: int, m: int, r: int, obs_coverage: float = 0.3):
        """
        Initializes a CityGrid with specified dimensions and tower coverage range.

        Args:
            n (int): Count of rows in the grid.
            m (int): Count of columns in the grid.
            r (int): The range of coverage for each tower.
            obs_coverage (float, optional): The proportion of obstructed blocks (default is 0.3).
        """
        assert n > 0, f"Count of rows need to be greater than zero"
        assert m > 0, f"Count of columns need to be greater than zero"
        assert r > 0, f"The range of coverage for each tower need to be greater than zero"

        self.n = n
        self.m = m
        self.tower_radius = r
        self.grid = [[0 for _ in range(m)] for _ in range(n)]
        self.towers = []
        self.generate_obstructions(obs_coverage)
        self.place_optimal_towers()

    def generate_obstructions(self, obs_coverage: float):
        """
        Generates obstructed blocks randomly based on the specified coverage proportion.

        Args:
            obs_coverage (float): The proportion of obstructed blocks.
        """
        count_of_obstructed_blocks = 0
        while count_of_obstructed_blocks < int(self.n * self.m * obs_coverage):
            random_n = randint(0, self.n - 1)
            random_m = randint(0, self.m - 1)
            if not self.grid[random_n][random_m]:
                self.grid[random_n][random_m] = 'X'
                count_of_obstructed_blocks += 1

    def place_tower(self, x: int, y: int, r: int):
        """
        Places a tower at the specified coordinates.

        Args:
            x (int): The row coordinate.
            y (int): The column coordinate.
            r (int): The range of coverage for the tower.
        """
        if self.grid[x][y] not in ['|', 'X']:
            self.grid[x][y] = '|'
            self.towers.append((x, y))
            print(f"Tower placed on ({x}, {y})")
            for i in range(max(0, x - r), min(self.n, x + r + 1)):
                for j in range(max(0, y - r), min(self.m, y + r + 1)):
                    if self.grid[i][j] == 0:
                        self.grid[i][j] = '#'
        else:
            print(f"This block occupied by {self.grid[x][y]!r}")

    def place_optimal_towers(self):
        """Places towers optimally to cover all available blocks."""
        uncovered_blocks = self.get_uncovered_blocks()
        while uncovered_blocks:
            best_tower_position = None
            best_coverage = 0
            for i in range(self.n):
                for j in range(self.m):
                    if self.grid[i][j] in ['#', 0]:
                        coverage = self.get_coverage(i, j, self.tower_radius)
                        if coverage > best_coverage:
                            best_tower_position = (i, j)
                            best_coverage = coverage
            if best_tower_position is not None:
                self.place_tower(best_tower_position[0], best_tower_position[1], self.tower_radius)
                self.display_info()
                uncovered_blocks = self.get_uncovered_blocks()

    def get_uncovered_blocks(self) -> list[tuple[int, int]]:
        """
        Returns a list of coordinates for uncovered blocks.

        Returns:
            list[tuple[int, int]]: List of coordinates for uncovered blocks.
        """
        uncovered_blocks = []
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 0:
                    uncovered_blocks.append((i, j))
        return uncovered_blocks

    def get_coverage(self, x: int, y: int, R: int):
        """
        Calculates the coverage of a tower at specified coordinates.

        Args:
            x (int): The row coordinate.
            y (int): The column coordinate.
            R (int): The range of coverage for the tower.

        Returns:
            int: The coverage count.
        """
        coverage = 0
        for i in range(max(0, x - R), min(self.n, x + R + 1)):
            for j in range(max(0, y - R), min(self.m, y + R + 1)):
                if self.grid[i][j] == 0:
                    coverage += 1
        return coverage

    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]] | None:
        """
        Finds a path between two towers with A*(A-star)

        Args:
            start (tuple[int, int]): The coordinates of the starting tower.
            end (tuple[int, int]): The coordinates of the ending tower.

        Returns:
            list[tuple[int, int]]: List of coordinates representing the path.
        """
        open_list = [(0, start, [])]
        closed_list = set()

        while open_list:
            _, (x, y), path = min(open_list)
            open_list.remove((_, (x, y), path))

            if (x, y) == end:
                return path + [(x, y)]

            if (x, y) in closed_list:
                continue

            closed_list.add((x, y))

            for i in range(max(0, x - 1), min(self.n, x + 2)):
                for j in range(max(0, y - 1), min(self.m, y + 2)):
                    if (i != x or j != y) and self.grid[i][j] in ['#', '|']:
                        open_list.append(
                            (len(path) + 1 + abs(i - end[0]) + abs(j - end[1]), (i, j), path + [(x, y)]))

        return None

    def build_path_on_grid(self, ttt_path: list[tuple[int, int]]):
        """
        Marks the tower to tower path on the grid.

        Args:
            ttt_path (list[tuple[int, int]]): List of coordinates representing the tower to tower path.
        """
        for cord in ttt_path[1:-1]:
            self.grid[cord[0]][cord[1]] = "*"
        else:
            self.grid[ttt_path[0][0]][ttt_path[0][1]] = "B"
            self.grid[ttt_path[-1][0]][ttt_path[-1][1]] = "E"

