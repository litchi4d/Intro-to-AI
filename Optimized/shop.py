from isort import output
from Search.main import get_neighbours
import random
class Space():
    def __init__(self,height,width,num_hospitals):
        self.height = height
        self.width = width
        self.num_hospitals = num_hospitals
        self.hospitals = set()
        self.houses = set()

    def add_house(self,row,col):
        self.houses.add((row,col))

    def availaible_space(self):
        candidates = set(
            (row,col)
            for row in range(self.height)
            for col in range(self.width)
        )
        for house in self.houses:
            candidates.remove(house)
        for hospital in self.hospitals:
            candidates.remove(hospital)
        return candidates
    def getCost(self, hospitals):
            """Calculates sum of distances from houses to nearest hospital."""
            cost = 0
            for house in self.houses:
                cost += min(
                    abs(house[0] - hospital[0]) + abs(house[1] - hospital[1])
                    for hospital in hospitals
                )
            return cost

    def output_image(self, filename):
        """Generates image with all houses and hospitals."""
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size,
            self.height * cell_size + cost_size + padding * 2),
            "white"
        )
        house = Image.open("assets/images/House.png").resize(
            (cell_size, cell_size)
        )
        hospital = Image.open("assets/images/Hospital.png").resize(
            (cell_size, cell_size)
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 30)
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):

                # Draw cell
                rect = [
                    (j * cell_size + cell_border,
                    i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                    (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="black")

                if (i, j) in self.houses:
                    img.paste(house, rect[0], house)
                if (i, j) in self.hospitals:
                    img.paste(hospital, rect[0], hospital)

        # Add cost
        draw.rectangle(
            (0, self.height * cell_size, self.width * cell_size,
            self.height * cell_size + cost_size + padding * 2),
            "black"
        )
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Cost: {self.getCost(self.hospitals)}",
            fill="white",
            font=font
        )

        img.save(filename)

    def get_neighbours(self, row, col):
        """Returns neighbors not already containing a house or hospital."""
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]
        neighbors = []
        for r, c in candidates:
            if (r, c) in self.houses or (r, c) in self.hospitals:
                continue
            if 0 <= r < self.height and 0 <= c < self.width:
                neighbors.append((r, c))
        return neighbors

    def hill_climbing(self,maximum = None, image_prefix = None, log = False):
        count =0;
        self.hospitals = set()
        for i in range(self.num_hospitals):
            self.hospitals.add(random.choice(list(self.availaible_space())))
        if(log):
            print(f"Initial state, score = {self.getCost(self.hospitals)}")
        if(image_prefix):
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")
        while maximum is None or count<maximum:
            count+=1
            best_neighbours = []
            best_neighbour_cost = -1
            for hospital in self.hospitals:
                for replace in self.get_neighbours(*hospital):
                    neighbor = self.hospitals.copy()
                    neighbor.remove(hospital)
                    neighbor.add(replace)
                    cost = self.getCost(neighbor)
                    if best_neighbour_cost is -1 or cost<best_neighbour_cost:
                        best_neighbors = [neighbor]
                        best_neighbour_cost = cost
                    elif cost == best_neighbour_cost:
                        best_neighbours.append(neighbor)
            if(best_neighbour_cost>=self.getCost(self.hospitals)):
                return self.hospitals
            else:
                if(log):
                    print(f"New state, score = {best_neighbour_cost}")
                self.hospitals = random.choice(best_neighbours)
        if(image_prefix):
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

# Create a new space and add houses randomly
s = Space(height=10, width=20, num_hospitals=3)
for i in range(15):
    s.add_house(random.randrange(s.height), random.randrange(s.width))

# Use local search to determine hospital placement
hospitals = s.hill_climbing(image_prefix="hospitals", log=True)
