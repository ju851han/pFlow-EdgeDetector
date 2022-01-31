import numpy as np
import matplotlib.pyplot as plt

FLOOR_VALUE = 0
WALL_VALUE = 1


def apply_dijkstra(img):
    point = (0, 3, 1)   # x, y, cost
    cost_matrix = np.zeros(img.shape)
    job_list = [point]

    plt.imshow(img, cmap="gray")
    plt.plot(0, 3, "ro")  # red o-marker
    # plt.show()
    while len(job_list) > 0:
        print("Liste = {}".format(job_list))
        point = job_list.pop(0)
        cost = point[2]
        if cost_matrix[point[1]][point[0]] != 0:
            continue  # already done
        cost_matrix[point[1]][point[0]] = cost
        neighbors = get_neighbors(point)
        for neighbor in neighbors:
            try:
                if neighbor[0] < 0 or neighbor[1] < 0:
                    continue     # IndexOutOfBounds without Exception
                value = img[neighbor[1]][neighbor[0]]
                # print(value)
                if value == FLOOR_VALUE:
                    continue    # connections are only possible through wall
                elif value == WALL_VALUE:
                    if cost_matrix[neighbor[1]][neighbor[0]] > 0:
                        continue    # point already visited
                    else:
                        job_list.append((neighbor[0], neighbor[1], cost+1))
                else:
                    raise Exception("Unreachable Code.")
            except IndexError:  # ignore IndexOutOfBounds
                continue
    plt.figure("Cost Matrix")
    plt.imshow(cost_matrix, cmap="gray")
    plt.show()


def get_neighbors(point):
    return [(point[0], point[1] - 1),
            (point[0] - 1, point[1]), (point[0] + 1, point[1]),
            (point[0], point[1] + 1)]


if __name__ == '__main__':
    img = np.array([[0, 0, 1, 1, 1],
                    [0, 1, 1, 1, 1],
                    [1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1]])

    apply_dijkstra(img)
