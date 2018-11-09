from tkinter import *
from enum import Enum

def init_canvas():
  canvas = Canvas(game, width=width, height=height, background='#fff')
  canvas.pack()

  canvas.create_rectangle(0, 0, width, height - 50, fill='#4259f4')
  return canvas

def findItemInGrid(id):
  for i in range(len(grid)):
    column = grid[i]

    for j in range(len(column)):
      row = column[j]

      if row['id'] == id:
        return {'column': i, 'row': j}
  return None

def nextStep():
  global currentPlayer

  if currentPlayer == State.PLAYER1:
    currentPlayer = State.PLAYER2
    status['text2'] = "Player 2"
    newColor = status['color2']
  else:
    currentPlayer = State.PLAYER1
    status['text2'] = "Player 1"
    newColor = status['color1']
  canvas.itemconfig(statusTextItem, text=(status['text1'] + status['text2']))
  canvas.itemconfig(statusColorItem, fill=newColor)

def onclick(event):
  item = event.widget.find_closest(event.x, event.y)[0]

  itemPos = findItemInGrid(item) 
  if itemPos is not None:
    nxt = False
    for row in grid[itemPos['column']]:
      if row['state'] == State.EMPTY:
        row['state'] = currentPlayer
        if currentPlayer == State.PLAYER1: canvas.itemconfig(row['id'], fill=status['color1'])
        else: canvas.itemconfig(row['id'], fill=status['color2'])
        nxt = True
        break
    if nxt: nextStep()


def draw_circle(canvas, posX, posY, size):
  return canvas.create_oval(posX, posY, posX + size, posY + size, fill='#fff')

def draw_grid(canvas, width, height, size, offset):
  columns = []

  for column in range(gridColumns):
    rows = []
    posX = offset + ((size + (offset * 2)) * column)

    for row in range(gridRows):
      posY = (height + offset) - ((size + (offset * 2)) * (row + 1))
      circle_id = draw_circle(canvas, posX, posY, size)
      canvas.tag_bind(circle_id, '<Button-1>', onclick)
      rows.insert(row, {'id': circle_id, 'state': State.EMPTY})
    
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
height = 550
draw_offset = 5
circle_size = 70

currentPlayer = State.PLAYER1
status = {'text1': "Current player: ", 'text2': "Player 1", 'color1': "#F00", 'color2': "#FF0"}

canvas = init_canvas()
statusTextItem = canvas.create_text(draw_offset * 2, height - 50 + draw_offset, text=(status['text1'] + status['text2']), anchor=NW)
statusColorItem = canvas.create_oval(draw_offset * 2 + 125, height - 50 + draw_offset, draw_offset * 2 + 125 + 15, height - 50 + draw_offset + 15, fill=status['color1'])
grid = draw_grid(canvas, width, height - 50, circle_size, draw_offset)

game.mainloop()
