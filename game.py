from tkinter import *
from enum import Enum

def init_canvas():
  canvas = Canvas(game, width=width, height=height, background="#fff")
  canvas.pack()

  canvas.create_rectangle(0, 0, width, height, fill="#4259f4")
  return canvas

def nextStep():
  global currentPlayer

  currentPlayer = State.PLAYER2 if currentPlayer == State.PLAYER1 else State.PLAYER1

def onclick(event):
  item = event.widget.find_closest(event.x, event.y)[0]
  if currentPlayer == State.PLAYER1: canvas.itemconfig(item, fill="#F00")
  else: canvas.itemconfig(item, fill="#FF0")

  # find element in  grid tuple, find column, check where to change state if possible, if not possible, don't progress

  nextStep()

def draw_circle(canvas, posX, posY, size):
  return canvas.create_oval(posX, posY, posX + size, posY + size, fill="#fff")

def draw_grid(canvas, width, height, size, offset):
  columns = []

  for column in range(gridColumns):
    rows = []
    posX = offset + ((size + (offset * 2)) * column)

    for row in range(gridRows):
      posY = (height + offset) - ((size + (offset * 2)) * (row + 1))
      # add id by creating oval
      circle_id = draw_circle(canvas, posX, posY, size)
      canvas.tag_bind(circle_id, '<Button-1>', onclick)
      rows.insert(row, {"id": circle_id, "state": State.EMPTY})
    
    columns.insert(column, tuple(rows))

  return tuple(columns)

class State(Enum):
  EMPTY = 0
  PLAYER1 = 1
  PLAYER2 = 2

grid = ()
gridColumns = 7
gridRows = 6

game = Tk()
game.configure(background='white')
game.title("Connect 4 by Matthijs Booman")

width = 600
height = 500
draw_offset = 5
circle_size = 70

currentPlayer = State.PLAYER1

canvas = init_canvas()
grid = draw_grid(canvas, width, height, circle_size, draw_offset)
print(grid)

game.mainloop()
