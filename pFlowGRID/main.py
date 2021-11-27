import math
import sys
import tkinter as tk
from tkinter import filedialog
import tri_utils as tri

window_width = "1300"
window_height = "610"
point_radius = 5

main_window = None
# TODO -1- Needs work for clean separation into classes
drawing_canvas: tk.Canvas = None

# buttons
finish_wall_points_btn: tk.Button = None
triangulate_btn: tk.Button = None
draw_holes_btn: tk.Button = None


# Labels are obstacles like tables etc
labels = []

wall_points = []
lines = []
to_be_moved_point_index = -1
# First No. of hole poly, second No. of point in poly
to_be_moved_hole_index = (-1, -1)

hole_poly_count = -1
hole_polys = []
hole_poly_lines = []

mesh = None
popup_open = False

state_saved = False
save_file_path = ""
currently_loaded_floor_plan = ""


def draw_wall_points(event):
    x, y = event.x, event.y

    current_color = 'red'
    if hole_poly_count >= 0:
        current_color = 'blue'

    point = drawing_canvas.create_oval([x - point_radius, y - point_radius,
                                        x + point_radius, y + point_radius],
                                       outline='black', fill=current_color)

    if hole_poly_count >= 0:
        global hole_polys
        hole_polys[hole_poly_count].append((x, y, point))
        current_point_list = hole_polys[hole_poly_count]
    else:
        global wall_points
        # x = X-Coord
        # y = Y-Coord
        # point is the ID of point in canvas (used to delete and redraw)
        wall_points.append((x, y, point))
        current_point_list = wall_points

    if len(current_point_list) > 1:
        to_be_drawn_points = current_point_list[-2:]
        p1 = to_be_drawn_points[0]
        p2 = to_be_drawn_points[1]

        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')

        if hole_poly_count >= 0:
            global hole_poly_lines
            hole_poly_lines[hole_poly_count].append(line)
        else:
            global lines
            lines.append(line)


def finish_wall_points():
    if hole_poly_count > -1 and len(hole_polys[hole_poly_count]) < 3:
        print('Cant finish, since not enough points have been placed.')
        return

    if len(wall_points) < 3:
        print('Cant finish, since not enough points have been placed.')
        return

    if hole_poly_count < 0:
        # Draw the last line between first and last given point
        p1 = wall_points[-1]
        p2 = wall_points[0]
        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
        global lines
        lines.append(line)
    else:
        current_wall_points = hole_polys[hole_poly_count]

        p1 = current_wall_points[-1]
        p2 = current_wall_points[0]
        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
        global hole_poly_lines
        hole_poly_lines[hole_poly_count].append(line)

    switch_editing_state(1)


def calculate_point_distance(click, point):
    """Calculates distance between given point and click event using pythagoras theorem"""
    x, y = click.x, click.y

    point_x = point[0]
    point_y = point[1]

    x_diff = abs(point_x - x)
    y_diff = abs(point_y - y)

    # pythagoras theorem
    current_distance = math.sqrt((x_diff ** 2) + (y_diff ** 2))

    return current_distance


def edit_wall_points(event):
    """Start of moving wall points.
    After a click on the canvas happens the distance between click and every point is calculated to see if the
    click clicked a point that will be moved in the second phase of moving wall points"""
    current_min_distance = sys.maxsize
    point_index_of_min_distance = 0

    # loop through wall points
    for i in range(len(wall_points)):
        # Find the point nearest to the mouse click
        current_distance = calculate_point_distance(event, wall_points[i])

        if current_distance < current_min_distance:
            current_min_distance = current_distance
            point_index_of_min_distance = i

    for i in range(len(hole_polys)):
        for j in range(len(hole_polys[i])):
            current_distance = calculate_point_distance(event, hole_polys[i][j])

            if current_distance < current_min_distance:
                current_min_distance = current_distance
                point_index_of_min_distance = (i, j)

    if current_min_distance < 8:
        # if click is in range of a button
        global to_be_moved_point_index, to_be_moved_hole_index

        if type(point_index_of_min_distance) is int:
            to_be_moved_point_index = point_index_of_min_distance
        else:
            to_be_moved_hole_index = point_index_of_min_distance


def edit_wall_points_drag_motion(event):
    """Clicked point and its lines are being redrawn at the dragging cursors location"""
    if to_be_moved_point_index == -1 and to_be_moved_hole_index[0] == -1:
        # if drag is without the click of a button before, drag does nothing
        return

    global wall_points, lines, hole_polys, hole_poly_lines
    x, y = event.x, event.y

    hole_moved = False
    point_color = 'red'
    if to_be_moved_point_index != -1:
        # main poly point is getting moved
        # define the old point with its lines
        p0 = wall_points[to_be_moved_point_index]
        l0 = lines[to_be_moved_point_index - 1]
        l1 = lines[to_be_moved_point_index]

    elif to_be_moved_hole_index[0] != -1:
        # hole poly point is moved
        hole_moved = True
        point_color = 'blue'

        p0 = hole_polys[to_be_moved_hole_index[0]][to_be_moved_hole_index[1]]
        l0 = hole_poly_lines[to_be_moved_hole_index[0]][to_be_moved_hole_index[1] - 1]
        l1 = hole_poly_lines[to_be_moved_hole_index[0]][to_be_moved_hole_index[1]]

    # draw new point
    new_p0_id = drawing_canvas.create_oval([x - point_radius, y - point_radius,
                                            x + point_radius, y + point_radius],
                                           outline='black', fill=point_color)
    # save point as tuple to prepare saving
    new_p0 = (x, y, new_p0_id)

    # wall point moved
    if not hole_moved:

        point_before_new_p0 = wall_points[to_be_moved_point_index - 1]
        # modulo needed here in case last point in list is clicked and the index (i + 1) overflows
        point_after_new_p0 = wall_points[(to_be_moved_point_index + 1) % len(wall_points)]

    else:
        point_before_new_p0 = hole_polys[to_be_moved_hole_index[0]][to_be_moved_hole_index[1] - 1]
        # modulo needed here in case last point in list is clicked and the index (i + 1) overflows
        point_after_new_p0 = hole_polys[to_be_moved_hole_index[0]][
            (to_be_moved_hole_index[1] + 1) % len(hole_polys[to_be_moved_hole_index[0]])]

    new_l0 = drawing_canvas.create_line([point_before_new_p0[0], point_before_new_p0[1],
                                         new_p0[0], new_p0[1]], fill='black')

    new_l1 = drawing_canvas.create_line([new_p0[0], new_p0[1],
                                         point_after_new_p0[0], point_after_new_p0[1]], fill='black')

    if not hole_moved:
        lines[to_be_moved_point_index - 1] = new_l0
        lines[to_be_moved_point_index] = new_l1
        wall_points[to_be_moved_point_index] = new_p0
    else:
        hole_poly_lines[to_be_moved_hole_index[0]][to_be_moved_hole_index[1] - 1] = new_l0
        hole_poly_lines[to_be_moved_hole_index[0]][to_be_moved_hole_index[1]] = new_l1
        hole_polys[to_be_moved_hole_index[0]][to_be_moved_hole_index[1]] = new_p0

    # deleting point that has been clicked and its lines
    drawing_canvas.delete(p0[2])
    drawing_canvas.delete(l0)
    drawing_canvas.delete(l1)


def edit_wall_points_drag_whole_poly(event):
    if to_be_moved_point_index == -1 and to_be_moved_hole_index[0] == -1:
        # if drag is without the click of a button before, drag does nothing
        return

    global wall_points, lines, hole_polys, hole_poly_lines
    x, y = event.x, event.y

    hole_moved = False
    point_color = 'red'

    if to_be_moved_point_index != -1:
        # main poly point is getting moved
        # define the old point
        p0 = wall_points[to_be_moved_point_index]

        change_in_x = x - p0[0]
        change_in_y = y - p0[1]

        for i in range(len(wall_points)):
            # drawing points
            point = wall_points[i]

            # delete old point point and line
            drawing_canvas.delete(point[2])

            # draw new point, save canvas id
            new_point = drawing_canvas.create_oval([point[0] + change_in_x - point_radius,
                                                    point[1] + change_in_y - point_radius,
                                                    point[0] + change_in_x + point_radius,
                                                    point[1] + change_in_y + point_radius],
                                                   outline='black', fill=point_color)

            # parse it back into wall_points
            wall_points[i] = (point[0] + change_in_x, point[1] + change_in_y, new_point)

        for i in range(len(wall_points)):
            # draw lines
            old_line = lines[i]
            drawing_canvas.delete(old_line)

            # i + 1 here, because line at j is line between point j and j + 1
            p0 = wall_points[i]
            p1 = wall_points[(i + 1) % len(wall_points)]

            line = drawing_canvas.create_line([p0[0], p0[1], p1[0], p1[1]], fill='black')
            lines[i] = line

    elif to_be_moved_hole_index[0] != -1:
        # hole poly point is moved
        point_color = 'blue'

        p0 = hole_polys[to_be_moved_hole_index[0]][to_be_moved_hole_index[1]]

        change_in_x = x - p0[0]
        change_in_y = y - p0[1]

        for i in range(len(hole_polys[to_be_moved_hole_index[0]])):
            # drawing points
            point = hole_polys[to_be_moved_hole_index[0]][i]

            # delete old point point and line
            drawing_canvas.delete(point[2])

            # draw new point, save canvas id
            new_point = drawing_canvas.create_oval([point[0] + change_in_x - point_radius,
                                                    point[1] + change_in_y - point_radius,
                                                    point[0] + change_in_x + point_radius,
                                                    point[1] + change_in_y + point_radius],
                                                   outline='black', fill=point_color)

            # parse it back into wall_points
            hole_polys[to_be_moved_hole_index[0]][i] = (point[0] + change_in_x, point[1] + change_in_y, new_point)

        for i in range(len(hole_polys[to_be_moved_hole_index[0]])):
            # draw lines
            old_line = hole_poly_lines[to_be_moved_hole_index[0]][i]
            drawing_canvas.delete(old_line)

            # i + 1 here, because line at j is line between point j and j + 1
            p0 = hole_polys[to_be_moved_hole_index[0]][i]
            p1 = hole_polys[to_be_moved_hole_index[0]][(i + 1) % len(hole_polys[to_be_moved_hole_index[0]])]

            line = drawing_canvas.create_line([p0[0], p0[1], p1[0], p1[1]], fill='black')
            hole_poly_lines[to_be_moved_hole_index[0]][i] = line


def edit_wall_points_released(_):
    """End of moving points. Important variables are back to default values."""
    # if Button-1 is released the click and drag indicator is set back to a default value
    global to_be_moved_point_index, to_be_moved_hole_index
    to_be_moved_point_index = -1
    to_be_moved_hole_index = (-1, -1)


def draw_additional_polygons():
    global hole_poly_count

    switch_editing_state(0)

    global hole_polys, hole_poly_lines
    hole_poly_count += 1
    hole_polys.append([])
    hole_polys[hole_poly_count] = []

    hole_poly_lines.append([])
    hole_poly_lines[hole_poly_count] = []


def start_mesh_config():
    """Popup for meshing configuration."""
    # Make sure there is only one popup open
    global popup_open
    if popup_open:
        return

    popup_open = True

    popup = tk.Toplevel()
    popup.wm_title("Meshing")
    popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

    selected = tk.IntVar()

    tk.Label(popup, text="Select preferred meshing granularity.").pack()

    r0 = tk.Radiobutton(popup, text="Coarse", value=0, variable=selected)
    r1 = tk.Radiobutton(popup, text="Medium", value=1, variable=selected)
    r2 = tk.Radiobutton(popup, text="Fine", value=2, variable=selected)

    r0.pack(padx=5, pady=5)
    r1.pack(padx=5, pady=5)
    r2.pack(padx=5, pady=5)

    mesh_btn = tk.Button(popup, text="Generate Mesh", command=lambda: triangulate(selected.get(), popup))
    mesh_btn.pack(padx=5, pady=5)


def close_popup(window):
    """Custom close function for mesh config popup"""
    global popup_open
    popup_open = False
    window.destroy()


def triangulate(granularity_level,
                config_popup,
                window_x_max=int(window_width),
                window_y_max=int(window_height)):
    """Function to start the meshing"""

    # Start to calculate the granularity
    # by finding the size of the polygon
    poly_x_max = poly_y_max = 0
    poly_x_min = poly_y_min = sys.maxsize

    for point in wall_points:
        x = point[0]
        y = point[1]

        poly_x_min = min(poly_x_min, x)
        poly_y_min = min(poly_y_min, y)

        poly_x_max = max(poly_x_max, x)
        poly_y_max = max(poly_y_max, y)

    poly_width = poly_x_max - poly_x_min
    poly_height = poly_y_max - poly_y_min

    # Configuration of granularity level
    granularity = 0
    if granularity_level == 0:
        # Coarse
        granularity = ((poly_width / 0.3) + (poly_height / 0.3)) / 2
    elif granularity_level == 1:
        # Normal
        granularity = ((poly_width / 3) + (poly_height / 3)) / 2
    elif granularity_level == 2:
        # Fine
        granularity = ((poly_width / 30) + (poly_height / 30)) / 2

    close_popup(config_popup)
    global mesh
    mesh = tri.calculate_mesh(granularity, window_x_max, window_y_max, wall_points, hole_polys)


def start_export():
    """Check if a mesh is already generated, before start of export."""
    if mesh is None:
        print("No mesh generated yet. Create a mesh and then try again.")
        return

    tri.export_mesh(mesh)


def load_floor_plan():
    global drawing_canvas

    file = tk.filedialog.askopenfilename(initialdir="./", title="Select file",
                                         filetypes=(("png files", "*.png"),
                                                    ("PNG files", "*.PNG"),
                                                    # ("PNG files", "*.PNG"),
                                                    # ("all files", "*.*")
                                                    ))

    img = tk.PhotoImage(file=file)

    drawing_canvas.config(width=img.width(), height=img.height())
    drawing_canvas.create_image(0, 0, anchor=tk.NW, image=img)
    drawing_canvas.pack(expand=tk.YES)

    global currently_loaded_floor_plan
    currently_loaded_floor_plan = file

    # Seems like a work around, investigate later
    # TODO this
    #drawing_canvas.update()
    #main_window.update_idletasks()
    #main_window.update()
    #main_window.mainloop()
    tk.mainloop()


def save_to_file():
    save = create_save_to_file_string()

    # .nsv -> nik save
    file = tk.filedialog.asksaveasfile(mode="w",
                                       defaultextension=".nsv",
                                       initialdir="./",
                                       title="Choose where to save the file",
                                       initialfile="save.nsv")

    if file is None:
        return

    file.write(save)
    file.close()

    global save_file_path, state_saved
    save_file_path = file.name
    state_saved = True


def save_to_file_quick():
    if len(save_file_path) > 0:
        with open(save_file_path, "w") as text_file:
            print(create_save_to_file_string(), file=text_file)
    else:
        save_to_file()


def load_from_file():
    # ToDo check if stuff is already saved
    # ToDo check if buttons are disabled at the right time
    # ToDo beim laden einer datei alles vorher resetten
    # ToDo state richtig setzen bei fertigem import

    file = tk.filedialog.askopenfilename(initialdir="./", title="Select nsv file",
                                         filetypes=(("nsv files", "*.nsv"),
                                                    ("all files", "*.*")))

    if len(file) == 0:
        return

    f = open(file, "r")

    global wall_points, lines, hole_polys, hole_poly_lines, hole_poly_count, drawing_canvas, save_file_path

    # deleting previously drawn structures
    for i in range(len(wall_points)):
        drawing_canvas.delete(wall_points[i][2])
        drawing_canvas.delete(lines[i])

    for i in range(len(hole_polys)):
        for j in range(len(hole_polys[i])):
            drawing_canvas.delete(hole_polys[i][j][2])
            drawing_canvas.delete(hole_poly_lines[i][j])

    # resetting important data structures
    wall_points = []
    lines = []

    hole_poly_count = -1
    hole_polys = []
    hole_poly_lines = []

    # start reading file
    number_of_holes = int(f.readline())

    # loaded floor plan
    line = f.readline()[:-1]
    if line != "-":
        img = tk.PhotoImage(file=line)

        drawing_canvas.config(width=img.width(), height=img.height())
        drawing_canvas.create_image(0, 0, anchor=tk.NW, image=img)
        drawing_canvas.pack(expand=tk.YES)
        global main_window
        drawing_canvas.update()

    # main poly
    node_count_main_poly = int(f.readline())
    for i in range(node_count_main_poly):
        line = f.readline().split("\t")
        x = int(line[0])
        y = int(line[1])

        # draw new point, save canvas id
        new_point_id = drawing_canvas.create_oval([x - point_radius,
                                                   y - point_radius,
                                                   x + point_radius,
                                                   y + point_radius],
                                                  outline='black', fill='red')

        wall_points.append((x, y, new_point_id))

    lines = draw_lines_between_points(wall_points)

    # holes
    for i in range(number_of_holes):
        node_count_current_hole = int(f.readline())

        hole_poly_count += 1
        hole_polys.append([])
        hole_poly_lines.append([])

        # one hole
        for j in range(node_count_current_hole):

            line = f.readline().split("\t")
            x = int(line[0])
            y = int(line[1])

            # draw new point, save canvas id
            new_point_id = drawing_canvas.create_oval([x - point_radius,
                                                       y - point_radius,
                                                       x + point_radius,
                                                       y + point_radius],
                                                      outline='black', fill='blue')

            hole_polys[hole_poly_count].append((x, y, new_point_id))

        hole_poly_lines[hole_poly_count].append([])
        hole_poly_lines[hole_poly_count] = draw_lines_between_points(hole_polys[hole_poly_count])

    switch_editing_state(1)
    save_file_path = file

    # TODO aufgehört beim parsen des main polys
    #  ggf das zeichnen von linien in the fnc wrappen, ad ich das oben auch brauche


def create_save_to_file_string():
    save = str(hole_poly_count + 1) + "\n"

    if len(currently_loaded_floor_plan) > 0:
        save += currently_loaded_floor_plan + "\n"
    else:
        save += "-\n"

    # count of nodes, then nodes
    save += str(len(wall_points)) + "\n"
    for point in wall_points:
        save += str(point[0]) + "\t" + str(point[1]) + "\n"

    # holes
    for i in range(hole_poly_count + 1):
        save += str(len(hole_polys[i])) + "\n"
        for point in hole_polys[i]:
            save += str(point[0]) + "\t" + str(point[1]) + "\n"

    return save


def draw_lines_between_points(points):
    """points is an array of tuples of points with [0] as x coords and [1] as y
    returns list of line ids"""

    drawn_lines = []
    for i in range(len(points)):

        p0 = points[i]
        p1 = points[(i + 1) % len(points)]

        line = drawing_canvas.create_line([p0[0], p0[1], p1[0], p1[1]], fill='black')
        drawn_lines.append(line)

    return drawn_lines


def switch_editing_state(state_id):
    """State 0: Creating polygon state
    State 1: Editing polygon state"""

    global drawing_canvas

    if state_id == 0:
        drawing_canvas.unbind('<Button-1>')
        drawing_canvas.unbind('<B1-Motion>')
        drawing_canvas.unbind('<ButtonRelease-1>')
        drawing_canvas.unbind('<Button-3>')
        drawing_canvas.unbind('<B3-Motion>')
        drawing_canvas.unbind('<ButtonRelease-3>')

        drawing_canvas.bind('<Button-1>', draw_wall_points)

        # global triangulate_btn, draw_holes_button, finish_button
        triangulate_btn.config(state='disabled')
        draw_holes_btn.config(state='disabled')
        finish_wall_points_btn.config(state='normal')

    elif state_id == 1:
        # Unbind drawing new points
        drawing_canvas.bind('<Button-1>', edit_wall_points)
        drawing_canvas.bind('<B1-Motion>', edit_wall_points_drag_motion)
        drawing_canvas.bind('<ButtonRelease-1>', edit_wall_points_released)

        drawing_canvas.bind('<Button-3>', edit_wall_points)
        drawing_canvas.bind('<B3-Motion>', edit_wall_points_drag_whole_poly)
        drawing_canvas.bind('<ButtonRelease-3>', edit_wall_points_released)

        # Apply new state to buttons
        triangulate_btn.config(state='normal')
        draw_holes_btn.config(state='normal')
        finish_wall_points_btn.config(state='disabled')


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('pFlow Map Creator')

        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="Save", command=save_to_file_quick)
        file_menu.add_command(label="Save As", command=save_to_file)
        file_menu.add_command(label="Open", command=load_from_file)
        file_menu.add_command(label="Export", command=start_export)
        file_menu.add_command(label="Load floor plan", command=load_floor_plan)

        menu_bar.add_cascade(label="File", menu=file_menu)

        self.config(background="#BBBBBB", menu=menu_bar)
        self.geometry("{0}x{1}".format(window_width, window_height))

        self.leftFrame = OwnFrame(self, True)
        self.rightFrame = OwnFrame(self, False)

        global main_window
        main_window = self

        self.mainloop()


class OwnFrame(tk.Frame):
    def __init__(self, parent, left):
        super().__init__(parent, width=200, height=600)
        self.left = left

        if left:
            # Code to run if Frame is on the left side ...
            self.grid(row=0, column=0, padx=2, pady=2)

            self.canvas = OwnCanvas(self)
            self.canvas.bind('<Button-1>', draw_wall_points)

            # TODO -1-
            global drawing_canvas
            drawing_canvas = self.canvas

        else:
            # here on the right side
            self.grid(row=0, column=1, padx=2, pady=2)

            tk.Label(self, text="Instructions:") \
                .grid(row=0, column=0, padx=0, pady=0)

            text = 'Start clicking on the canvas to create corners of a polygon.\n' + \
                   'Once finished press the \'Finish Points\' Button to draw the\n' + \
                   'last line and finish the current polygon. Buttons may be\n' + \
                   'moved by drag and drop. To draw holes click the \'Draw Holes\'\n' + \
                   'Button and start clicking on the canvas.\n\n' + \
                   'You may import a floor plan as background to make the drawing easier\n' + \
                   'in the \'File\' menu. A mesh of the polygon and its holes may be\n' + \
                   'generated by pressing \'Calculate Mesh\' button. The mesh can be\n' + \
                   'saved by clicking \'Export\' in the \'File\' Menu.\n' + \
                   'Export will be saved as \'export.nik\'.'

            instructions = tk.Label(self, text=text)
            instructions.grid(row=1, column=0, padx=5, pady=20)

            global triangulate_btn, draw_holes_btn, finish_wall_points_btn

            triangulate_btn = tk.Button(self, text='Calculate Mesh', command=start_mesh_config, state=tk.DISABLED)

            draw_holes_btn = tk.Button(self,
                                       text='Draw holes',
                                       command=lambda: draw_additional_polygons(),
                                       state=tk.DISABLED)

            finish_wall_points_btn = tk.Button(self,
                                               text='Finish Points',
                                               command=lambda: finish_wall_points())

            finish_wall_points_btn.grid(row=2, column=0, pady=5)
            triangulate_btn.grid(row=3, column=0, pady=5)
            draw_holes_btn.grid(row=4, column=0, pady=5)


class OwnCanvas(tk.Canvas):
    def __init__(self, parent):
        width = 800
        height = 600
        super().__init__(parent, width=width, height=height, bg='white')
        self.grid(row=0, column=0)


def main():
    MainWindow()


if __name__ == "__main__":
    main()
