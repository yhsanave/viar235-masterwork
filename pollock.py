import cairo, math, random, argparse

float_gen = lambda a, b: random.uniform(a, b)
colors = []

# Move a random distance within a given range and a random angle
def randmove(cr, rmin, rmax, amin=0, amax=359):
    dist = float_gen(rmin, rmax)
    angle = math.radians(random.randint(amin, amax))
    dx = dist * math.cos(angle)
    dy = dist * math.sin(angle)
    return dx, dy

# Technique definitions

# Pour: a stroke that can vary in thickness
def pour(cr):
    length = random.randint(1,6)
    direction = random.randint(0,359)
    width = float_gen(scale * .01, scale * .05)
    for i in range(length):
        width += float_gen(-scale * .05, scale * .05)
        prevdir = direction
        direction += random.randint(-20, 20)
        
        splatter(cr, 5, scale * .01, scale * .03)
        dx, dy = randmove(cr, scale * .1, scale * .2, direction - 20, direction + 20)
        dx2, dy2 = randmove(cr, scale * .05, scale * .1, prevdir, prevdir) 
        cr.set_line_width(width)
        cr.rel_curve_to(dx2, dy2, dx2, dy2, dx, dy)

# Flick: A fast, short stroke with a lot of splatter
def flick(cr):
    distance = float_gen(scale * .1, scale * .3)
    angle = random.randint(0,359)
    for i in range(15):
        dx, dy = randmove(cr, distance/15, distance/15, angle - 30, angle + 30)
        cr.rel_move_to(dx, dy)
        splatter(cr, 5, scale * .05, scale * .1)

# Drop: A large, ellipsoid drop of color
def drop(cr):
    minor = float_gen(scale * .05, scale * .1)
    major = float_gen(scale * .05, scale * .1)
    angle = random.randint(0,359)
    
    x = cr.get_current_point()[0]
    y = cr.get_current_point()[1]
    cr.new_path()
    cr.translate(x, y)
    cr.rotate(angle)
    cr.scale(major / 2.0, minor / 2.0)
    cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
    cr.fill()
    cr.identity_matrix()
    cr.move_to(x, y)

# Drip: A stroke that decreases in thickness
def drip(cr):
    splatter(cr, 3, scale * .01, scale * .03)
    length = random.randint(1,6)
    direction = random.randint(0,359)
    width = float_gen(scale * .01, scale * .05)
    for i in range(length):
        width += float_gen(-scale * .05, 0)
        prevdir = direction
        direction += random.randint(-20, 20)
        
        splatter(cr, 5, scale * .01, scale * .03)
        dx, dy = randmove(cr, scale * .1, scale * .2, direction - 20, direction + 20)
        dx2, dy2 = randmove(cr, scale * .05, scale * .1, prevdir, prevdir) 
        cr.set_line_width(width)
        cr.rel_curve_to(dx2, dy2, dx2, dy2, dx, dy)

tech = [pour] * 5 + [flick] * 5 + [drop] * 1 + [drip] * 5

# Random splatter function
def splatter(cr, factor, rmin, rmax):
    check = factor - random.randint(0, 10)
    if check > 0:
        for i in range(check):
            current = cr.get_current_point()
            dx, dy = randmove(cr, rmin, rmax)
            cr.rel_move_to(dx, dy)
            cr.set_line_width(random.randint(int(scale * .005), int(scale * .01)))
            cr.rel_line_to(0,0)
            cr.stroke()
            cr.move_to(current[0],current[1])

# Draw function
def draw(cr):
    color = random.choice(colors)
    cr.set_source_rgb(float(color[0]), float(color[1]), float(color[2]))
    cr.move_to(float_gen(0,width), float_gen(0,height))
    for i in range(int(ops/2), int(ops*1.5)):
        random.choice(tech)(cr)
    

def main():
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default=1920, type=int)
    parser.add_argument("--height", default=1080, type=int)
    parser.add_argument("-c", "--colors", default=10, type=int)
    parser.add_argument("-d", "--depth", default=1000, type=int)
    parser.add_argument("-bg", "--background", default="none", type=str)
    parser.add_argument("-op", "--operations", default=3, type=int)
    parser.add_argument("-o", "--output", default="pollock", type=str)
    parser.add_argument("-mc", "--manualcolor", default="none", type=str)
    args = parser.parse_args()

    global width, height, depth, ops
    width, height = args.width, args.height
    depth = args.depth
    bg = args.background
    ops = args.operations
    
    global scale
    scale = (height + width) / 2

    # Initialize image and context
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)
    cr.set_line_join(cairo.LineJoin.ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)

    # Choose colors
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
            colors.append((float_gen(0, 1), float_gen(0, 1), float_gen(0, 1)))

    # Set background color
    if bg == "white":
        cr.set_source_rgb(1, 1, 1)
    elif bg == "black":
        cr.set_source_rgb(0, 0, 0)
    elif bg == "grey":
        cr.set_source_rgb(0.5, 0.5, 0.5)
    else:
        cr.set_source_rgba(0, 0, 0, 0)
    
    cr.rectangle(0, 0, width, height)
    cr.fill()
    
    # Draw shapes
    for i in range(depth):
        draw(cr)

    # Output
    ims.write_to_png(f"{args.output}.png")

if __name__ == "__main__":
    main()
