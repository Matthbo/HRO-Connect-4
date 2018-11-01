from tkinter import *

def init_canvas():
  canvas = Canvas(game, width=width, height=height, background="#fff")
  canvas.pack()

  canvas.create_rectangle(draw_offset, draw_offset, width - draw_offset, height - draw_offset, fill="#4259f4")
  return canvas

def draw_circle(posX, posY, size):
  return canvas.create_oval(posX, posY, posX + size, posY + size, fill="#fff")

def draw_grid(width, height):
  columns = []

  for column in range(gridColumns):
    rows = []

    for row in range(gridRows):
      # add id by creating oval
      #circle_id = draw_circle()
      rows.insert(row, {"state": ""})
    
    columns.insert(column, tuple(rows))

  return tuple(columns)

def test(event):
  item = event.widget.find_closest(event.x, event.y)[0]
  canvas.itemconfig(item, fill="#F00")
  # canvas.delete(item)

grid = ()
gridColumns = 7
gridRows = 6

game = Tk()
game.configure(background='white')
game.title("Connect 4 by Matthijs Booman")

width = 600
height = 600
draw_offset = 5
circle_size = 60

canvas = init_canvas()
grid = draw_grid()
print(grid)
#oval = draw_circle()
#canvas.tag_bind(oval, '<Button-1>', test)

#game.mainloop()
