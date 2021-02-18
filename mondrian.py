import cairo, math, random, argparse

colors = []

class Tile():
    def __init__(self,x,y):
        self.posx = x
        self.posy = y
        self.height = random.randint(1,5)
        self.width = random.randint(1,5)
        self.id = len(tiles)

        if random.randint(0,99) <= colordensity:
            self.color = random.choice(colors)
        else:
            self.color = [1, 1, 1]

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

def main():
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--resolution", default="1000x1000", type=str)
    parser.add_argument("-g", "--grid", default="10x10", type=str)
    parser.add_argument("-c", "--colors", default=3, type=int)
    parser.add_argument("-o", "--output", default="mondrian", type=str)
    parser.add_argument("-mc", "--manualcolor", default="none", type=str)
    parser.add_argument("-cd", "--colordensity", default=30, type=int)
    args = parser.parse_args()

    global res, gs, colordensity
    res = args.resolution.split("x")
    gs = args.grid.split("x")
    colordensity = args.colordensity

    # Use manual color file or generate random colors
    if args.manualcolor != "none":
        try:
            colorfile = open(args.manualcolor, "r")
            for l in colorfile:
                colors.append(l.split(','))
            colorfile.close()
        except:
            print(f"Color file {args.manualcolor} not found")
            exit()
    else:
        for i in range(args.colors):
            colors.append([random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)])

    # Initialize image surface and context
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(res[0]), int(res[1]))
    cr = cairo.Context(ims)

    # Background
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(0, 0, int(res[0]), int(res[1]))
    cr.fill()

    # Create Grid
    global grid
    grid = []
    for i in range(int(gs[1])):
        row = []
        for j in range(int(gs[0])):
            row.append(False)
        grid.append(row)

    # Grid Scale
    scalex = int(int(res[0]) / int(gs[0]))
    scaley = int(int(res[1]) / int(gs[1]))
    cr.set_line_width((scalex + scaley) / 20)

    # Generate tiles
    global tiles
    tiles = []
    for i in range(int(gs[1])):
        for j in range(int(gs[0])):
            if not grid[i][j]:
                tile = Tile(j,i)
                # Prevent tile overlaps
                for x in range(tile.width):
                    if j + x == int(gs[0]):
                        tile.set_width(x)
                        break
                
                    if grid[i][j+x]:
                        tile.set_width(x)
                        break

                for y in range(tile.height):
                    if i + y == int(gs[1]):
                        tile.set_height(y)
                        break
                
                # Set filled grid spaces
                for y in range(tile.height):
                    for x in range(tile.width):
                        grid[i+y][j+x] = True

                tiles.append(tile)

    # Draw
    for tile in tiles:
        cr.rectangle(tile.posx * scalex, tile.posy * scaley, tile.width * scalex, tile.height * scaley)
        cr.set_source_rgb(float(tile.color[0]),float(tile.color[1]),float(tile.color[2]))
        cr.fill_preserve()
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()

    # Output
    ims.write_to_png(f'{args.output}.png')

if __name__ == "__main__":
    main()