class Segmentation:

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

            borders = list(map(int, lines[j].strip().split()))
            self.xmax = borders[0]
            self.xmin = borders[1]
            self.ymax = borders[2]
            self.ymin = borders[3]

    def get_borders(self):
        return [self.xmax, self.xmin, self.ymax, self.ymin]

    def get_point_code(self, x, y):
        code = 0
        if y > self.ymax:
            code += 8
        else:
            code += 0

        if y < self.ymin:
            code += 4
        else:
            code += 0

        if x > self.xmax:
            code += 2
        else:
            code += 0

        if x < self.xmin:
            code += 1
        else:
            code += 0

        return code

    def peresechenie(self, num):
        if num & 0b1000:
            return 3
        elif num & 0b0100:
            return 2
        elif num & 0b0010:
            return 1
        elif num & 0b0001:
            return 0
        else:
            return -1

    def execute(self):
        result = []

        for segment in self.segments:
            ans = self.koen(segment[0], segment[1], segment[2], segment[3])
            if ans is not None:
                result.append(ans)

        return result

    def koen(self, x1, y1, x2, y2):
        p1 = self.get_point_code(x1, y1)
        p2 = self.get_point_code(x2, y2)

        if p1 == p2 == 0:
            return [x1, y1, x2, y2]

        if (p1 & p2) != 0:
            return None

        if ((p1 == 0 and p2 != 0) or (p2 == 0 and p1 != 0)) or (p1 & p2) == 0:
            k = (y2 - y1) / (x2 - x1)

            while True:
                if p1 == 0:
                    temp = p2
                    p2 = p1
                    p1 = temp
                    temp = x2
                    x2 = x1
                    x1 = temp
                    temp = y2
                    y2 = y1
                    y1 = temp

                if self.peresechenie(p1) == 3:
                    x1 = x1 + (1 / k) * (self.ymax - y1)
                    y1 = self.ymax
                elif self.peresechenie(p1) == 2:
                    x1 = x1 + (1 / k) * (self.ymin - y1)
                    y1 = self.ymin
                elif self.peresechenie(p1) == 1:
                    y1 = y1 + k * (self.xmax - x1)
                    x1 = self.xmax
                elif self.peresechenie(p1) == 0:
                    y1 = y1 + k * (self.xmin - x1)
                    x1 = self.xmin

                p1 = self.get_point_code(x1, y1)

                if p1 == p2 == 0:
                    return [x1, y1, x2, y2]

                if (p1 & p2) != 0:
                    return None