class KirusBack:
    def __init__(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

            num_lines = int(lines[0].strip())
            j = 1

            self.segments = []
            for i in range(num_lines):
                segment = list(map(int, lines[i + j].strip().split()))
                self.segments.append(segment)

            j += num_lines
            num_edges = int(lines[j].strip())
            j += 1

            self.polygon = []
            for i in range(num_edges):
                segment = list(map(int, lines[i + j].strip().split()))
                self.polygon.append(Point(segment[0], segment[1]))

    def give_option_number(self):
        return 1

    def option_poligon(self, option):
        if option == 1:
            self.polygon = [Point(0, 4), Point(1, 0), Point(5, 0), Point(6, 4), Point(3, 6)]

    def execute(self):
        result = []

        for segment in self.segments:
            ans = self.kirus_back(segment[0], segment[1], segment[2], segment[3])
            if ans is not None:
                result.append(ans)

        return result

    def kirus_back(self, px1, py1, px2, py2):
        tl, te = [1], [0]

        direction = Point(px2 - px1, py2 - py1)
        for i in range(len(self.polygon)):
            edge_start = self.polygon[i]
            edge_end = self.polygon[(i + 1) % len(self.polygon)]
            normal = self.normal_vector(Point(edge_start.x, edge_start.y), Point(edge_end.x, edge_end.y))

            scalar = self.scalar_product(normal, direction)
            if scalar == 0:
                continue

            t = (self.scalar_product(normal, Point(edge_start.x - px1, edge_start.y - py1)) / scalar)
            if scalar > 0:
                te.append(t)
            else:
                tl.append(t)

        max_te, min_tl = max(te), min(tl)
        if max_te > min_tl:
            return None

        return [px1 + max_te * direction.x, py1 + max_te * direction.y,
                px1 + min_tl * direction.x, py1 + min_tl * direction.y]

    def normal_vector(self, point1, point2):

        direction_vector = [point2.x - point1.x, point2.y - point1.y]
        normal_vector = Point(-direction_vector[1], direction_vector[0])

        return normal_vector

    def scalar_product(self, p1, p2):
        return p1.x * p2.x + p1.y * p2.y


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y