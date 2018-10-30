from tkinter import *
import time # temp

def init_canvas():
  canvas = Canvas(game, width=width, height=height, background="#fff")
  canvas.pack()

  canvas.create_rectangle(draw_offset, draw_offset, width - draw_offset, height - draw_offset, fill="#4259f4")
  return canvas

def draw_cirlce():
  offset = draw_offset * 2
  return canvas.create_oval(offset, offset, offset + 200, offset + 200, fill="#fff")

def draw_grid():
  pass

def test(event):
  item = event.widget.find_closest(event.x, event.y)[0]
  canvas.itemconfig(item, fill="#F00")
  # canvas.delete(item)

game = Tk()
game.configure(background='white')
game.title("Connect 4 by Matthijs Booman")

width = 600
height = 600
draw_offset = 5

canvas = init_canvas()
# draw_grid()
oval = draw_cirlce()
canvas.tag_bind(oval, '<Button-1>', test)

game.mainloop()



