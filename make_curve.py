from shapes import circle,ellipse,line,rectangle,star,polygon
def make_curve(name,polyline):
    if name=="circle":
        return circle.circle(polyline)
    elif name =="ellipse":
        return ellipse.ellipse(polyline)
    elif name =="rectangle":
        return rectangle.rectangle(polyline)
    elif name =="line":
        return line.line(polyline)
    elif name =="star":
        return star.star(polyline)
    elif name =="triangle":
        return polygon.polygon(points=polyline,num_sides=3)
    elif name =="square":
        return polygon.polygon(points=polyline,num_sides=4)
    elif name =="pentagon":
        return polygon.polygon(points=polyline,num_sides=5)
    elif name =="hexagon":
        return polygon.polygon(points=polyline,num_sides=6)
        
    