"""Script to generate different specifications of random points inside a given mesh.

3 configurations are support at the moment

1: Generate middle point for each triangle.
2: Generate a random point in each triangle
3: Generate random amount of points (configured by the "count" parameter, 0 defaults to amount of triangles)
in random triangles"""
import os
import random

amount_of_random_generated_triangles = 2000


def generate_points():
    nodes, triangles = import_mesh()

    path = str(os.getcwd()) + "/random_points"
    if not os.path.exists(path):
        os.mkdir(path)

    generate_middle_points(nodes, triangles)
    generate_random_points(nodes, triangles)
    generate_random_points_in_random_triangles(nodes, triangles, count=amount_of_random_generated_triangles)


def generate_middle_points(nodes, triangles):
    """Generate middle points, one for each triangle."""

    # generating middle points of the triangles
    middle_points = []
    export_string = ''

    for tri in triangles:
        # copy may be obsolete here
        tri_copy = tri.copy()
        p0 = nodes[tri_copy.pop()]
        p1 = nodes[tri_copy.pop()]
        p2 = nodes[tri_copy.pop()]

        middle_x = (p0[0] + p1[0] + p2[0]) / 3
        middle_y = (p0[1] + p1[1] + p2[1]) / 3
        # middle_points.append((middle_x, middle_y))
        export_string += str(middle_x) + '\t' + str(middle_y) + '\n'

    with open("random_points/middle_points.txt", "w") as out:
        print(export_string, file=out)


def generate_random_points(nodes, triangles):
    """Generate a random point in each triangle"""

    random_points = []
    export_string = ''

    for tri in triangles:
        # copy may be obsolete here
        tri_copy = tri.copy()
        p0 = nodes[tri_copy.pop()]
        p1 = nodes[tri_copy.pop()]
        p2 = nodes[tri_copy.pop()]

        # idea found at https://stackoverflow.com/questions/5563808/how-to-generate-three-random-numbers-whose-sum-is-1

        r0 = random.uniform(0, 1)
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        factor = 1 / (r0 + r1 + r2)
        f0 = r0 * factor
        f1 = r1 * factor
        f2 = r2 * factor

        rand_x = p0[0] * f0 + p1[0] * f1 + p2[0] * f2
        rand_y = p0[1] * f0 + p1[1] * f1 + p2[1] * f2

        # random_points.append((rand_x, rand_y))
        export_string += str(rand_x) + '\t' + str(rand_y) + '\n'

    with open("random_points/random_points.txt", "w") as out:
        print(export_string, file=out)


def generate_random_points_in_random_triangles(nodes, triangles, count=0):
    """Generate n points (default n is for every triangle once) in a random location inside a random triangle."""

    # count defaults to length of triangles
    if count == 0:
        count = len(triangles)

    export_string = ''

    for i in range(count):
        # get a random triangle
        rand_triangle = triangles[random.randrange(0, len(triangles))]

        # copy may be obsolete here
        tri_copy = rand_triangle.copy()
        p0 = nodes[tri_copy.pop()]
        p1 = nodes[tri_copy.pop()]
        p2 = nodes[tri_copy.pop()]

        # idea found at https://stackoverflow.com/questions/5563808/how-to-generate-three-random-numbers-whose-sum-is-1
        # Random numbers between 0 and 1
        r0 = random.uniform(0, 1)
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        factor = 1 / (r0 + r1 + r2)
        f0 = r0 * factor
        f1 = r1 * factor
        f2 = r2 * factor

        rand_x = p0[0] * f0 + p1[0] * f1 + p2[0] * f2
        rand_y = p0[1] * f0 + p1[1] * f1 + p2[1] * f2

        # random_points.append((rand_x, rand_y))
        export_string += str(rand_x) + '\t' + str(rand_y) + '\n'

    with open("random_points/random_points_random_triangles.txt", "w") as out:
        print(export_string, file=out)


def import_mesh():
    # ToDo make it read default export path
    with open("../export.nik", "r") as f:

        first_line = f.readline().split('\t')

        node_count = int(first_line[0])
        triangle_count = int(first_line[1])

        # Reading triangles
        triangles = []
        for i in range(triangle_count):
            split_line = f.readline().split('\t')

            tri_set = {int(split_line[0]), int(split_line[1]), int(split_line[2])}
            triangles.append(tri_set)

        # Reading nodes
        nodes = []
        for i in range(node_count):
            split_line = f.readline().split('\t')
            nodes.append((float(split_line[0]), float(split_line[1])))

    return nodes, triangles


if __name__ == "__main__":
    generate_points()
