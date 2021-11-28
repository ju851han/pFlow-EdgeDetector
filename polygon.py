from tkinter import filedialog


class Polygon:
    def __init__(self):
        """
        Constructor
        """
        self.points = []
        self.border_color = 'black'

    def add_point(self, x, y):
        """
        Sets a node (=point, corner)
        :param x: x-coordinate
        :param y: y-coordinate
        :return: None
        """
        self.points.append((x, y))

    def __transform_pointlist_to_saving_string(self):
        """
        Converts a pointlist into a string which is later saved in a file
        Origin method: pFlowGRID.main.create_save_to_file_string()
        :return: str
        """
        # save = str(hole_poly_count + 1) + "\n"

        # if len(currently_loaded_floor_plan) > 0:
        #   save += currently_loaded_floor_plan + "\n"
        # else:
        #   save += "-\n"

        save = "0\n-\n"  # TODO wenn Hindernisse im Grundrisse erstellt werden, diese Zeile löschen und Kommentare einkommentieren
        # count of nodes, then nodes
        save += str(len(self.points)) + "\n"
        for point in self.points:
            save += str(point[0]) + "\t" + str(point[1]) + "\n"

        # holes
        # for i in range(hole_poly_count + 1):
        #    save += str(len(hole_polys[i])) + "\n"
        #   for point in hole_polys[i]:
        #      save += str(point[0]) + "\t" + str(point[1]) + "\n"

        return save

    def save_to_file(self, file=None):
        """
        Writes and saves the saving_string into the file.
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

        file.write(self.__transform_pointlist_to_saving_string())
        file.close()
