from tkinter import filedialog


class Polygon:
    def __init__(self):
        """Constructor

        """
        self.points = []
        self.border_color = 'black'
        self.inner_polygons = []

    def add_inner_polygons(self, polygon):
        """Adds an inner-polygon into the list of an outer-polygon.

        Inner_polygons can be obstacles.
        :param polygon: Polygon
        :return: None
        """
        self.inner_polygons.append(polygon)

    def add_point(self, x, y):
        """Sets a node (=point, corner) and adds it to a list

        :param x: x-coordinate
        :param y: y-coordinate
        :return: None
        """
        self.points.append((x, y))

    @property
    def __transform_pointlist_to_saving_string(self):
        """Converts a points into a string which is later saved in a file.

        Origin method: pFlowGRID.main.create_save_to_file_string()
        :return: str
        """
        save = str(len(self.inner_polygons)) + "\n"

        # if len(currently_loaded_floor_plan) > 0:
        #   save += currently_loaded_floor_plan + "\n"
        # else:
        save += "-\n"

        # count of nodes, then nodes
        save += str(len(self.points)) + "\n"
        for point in self.points:
            save += str(point[0]) + "\t" + str(point[1]) + "\n"

        # holes or obstacles
        for polygon in self.inner_polygons:
            save += str(len(polygon.points)) + "\n"
            for point in polygon.points:
                save += str(point[0]) + "\t" + str(point[1]) + "\n"

        return save

    def save_to_file(self, file=None):
        """Writes and saves the saving_string into the file.

        Origin method: pFlowGRID.main.save_to_file()
        File ending .nsv is used by pFlow.
        :param file: path of the file
        :return: None
        """
        # .nsv -> nik save
        if file is None:
            file = filedialog.asksaveasfile(mode="w",
                                            defaultextension=".nsv",
                                            initialdir="./",
                                            title="Choose where to save the file",
                                            initialfile="save.nsv")
        else:
            file = open(file=file, mode="w")
        if file is None:
            return

        file.write(self.__transform_pointlist_to_saving_string)
        file.close()
