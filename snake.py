import tkinter as tk
import random


global Width, Height, Map, TypeNum, TypeColor, FPS
Width = 20
Height = 20
Map = [[0 for i in range(Width)] for i in range(Height)]
TypeNum = {'ground': 0, 'snake': 1, 'food': 2, 'wall': 3}
TypeColor = {'ground': 'silver', 'snake': 'pink', 'food': 'yellow', 'wall': 'black'}
FPS = 150

Unit_size = 20


def draw_unit(canvas, x, y, type, size=20):
    x1 = x * size
    y1 = y * size
    x2 = (x + 1) * size
    y2 = (y + 1) * size
    canvas.create_rectangle(x1, y1, x2, y2, fill=TypeColor[type], outline='white')
    Map[x][y] = TypeNum[type]


class Background:
    def __init__(self, canvas, wall):
        self.ground_color = 'silver'
        self.wall_color = 'black'
        self.canvas = canvas
        self.wall = wall

    def draw(self):
        for x in range(Width):
            for y in range(Height):
                draw_unit(self.canvas, x, y, 'ground')
        for unit in self.wall:
            draw_unit(self.canvas, unit[0], unit[1], 'wall')


class Snake:
    def __init__(self, canvas, body, fps):
        self.canvas = canvas
        self.body = body
        assert len(body) > 1
        self.fps = fps
        # dir -1 for up, 1 for down, -2 for left, 2 for right
        self.dir = -2

    def draw(self):
        for unit in self.body:
            draw_unit(self.canvas, unit[0], unit[1], 'snake')

    def move(self):
        newbody = [0, 0]
        if self.dir % 2 == 0:
            newbody[1] = self.body[0][1]
            newbody[0] = self.body[0][0] + self.dir // 2
        else:
            newbody[0] = self.body[0][0]
            newbody[1] = self.body[0][1] + self.dir
        self.body.insert(0, newbody)

        # out of map
        if newbody[0] < 0 or newbody[0] >= len(Map) or newbody[1] < 0 or newbody[1] >= len(Map[0]):
            return 0

        newplace = Map[newbody[0]][newbody[1]]
        if newplace == TypeNum['snake'] or newplace == TypeNum['wall']:
            return 0
        elif newplace == TypeNum['food']:
            draw_unit(self.canvas, self.body[0][0], self.body[0][1], 'snake')
            set_food(self.canvas)
        else:
            draw_unit(self.canvas, self.body[-1][0], self.body[-1][1], 'ground')
            draw_unit(self.canvas, self.body[0][0], self.body[0][1], 'snake')
            self.body.pop()
        return 1

    def callback(self, event):
        key = event.keysym
        if key == 'Up' and self.dir != 1:
            self.dir = -1
        elif key == 'Down' and self.dir != -1:
            self.dir = 1
        elif key == 'Left' and self.dir != 2:
            self.dir = -2
        elif key == 'Right' and self.dir != -2:
            self.dir = 2


def set_food(canvas):
    ground_list = []
    for x in range(Width):
        for y in range(Height):
            if Map[x][y] == TypeNum['ground']:
                ground_list.append([x, y])
    food_loc = random.choice(ground_list)
    draw_unit(canvas, food_loc[0], food_loc[1], 'food')


def window_center(win, width, height):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    left = (screen_w - width) // 2
    top = (screen_h - height) // 2
    win.geometry("%dx%d+%d+%d"%(width, height, left, top))


def game_loop():
    win.update()
    if snake.move() == 0:
        over_lavel = tk.Label(win, text='Game Over', font=('Times', 25), width=15, height=1)
        over_lavel.place(x=60, y=Height / 2, bg=None)
        return
    win.after(FPS, game_loop)


if __name__ == "__main__":
    # create window
    win = tk.Tk()
    win.focus_force()
    win.resizable(False, False)
    win.title('Snake')
    window_center(win, Width*Unit_size, Height*Unit_size)
    canvas = tk.Canvas(win, width=Width*Unit_size, height=Height*Unit_size)
    canvas.pack()

    # create background
    wall = [[7, 7], [9, 7], [11, 7]]
    background = Background(canvas, wall)
    background.draw()

    # create snake
    body = [[8, 9], [9, 9], [10, 9]]
    snake = Snake(canvas, body, FPS)
    snake.draw()

    set_food(canvas)

    canvas.focus_set()
    canvas.bind("<KeyPress-Left>", snake.callback)
    canvas.bind("<KeyPress-Right>", snake.callback)
    canvas.bind("<KeyPress-Up>", snake.callback)
    canvas.bind("<KeyPress-Down>", snake.callback)

    game_loop()
    win.mainloop()
