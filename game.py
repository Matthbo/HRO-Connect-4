from tkinter import *
from enum import Enum

def init_canvas():
  canvas = Canvas(game, width=width, height=height, background='#fff')
  canvas.pack()

  canvas.create_rectangle(0, 0, width, height - 50, fill='#4259f4')
  return canvas

def stop():
  popupWindow.destroy()
  game.destroy()

def win():
  global popupWindow
  popupWindow = Toplevel(game)
  popupWindow.resizable(False, False)
  popupWindow.wait_visibility()
  popupWindow.grab_set()

  popupCanvas = Canvas(popupWindow, width=300, height=100)
  popupCanvas.pack()
  playerName = "Player 1" if currentPlayer == State.PLAYER1 else "Player 2"
  popupCanvas.create_text(draw_offset * 2, draw_offset * 2, text=(playerName + " Has Won!"), font=("Helvetica", 20), anchor=NW)
  btn = Button(popupWindow, text="Quit", command=stop)
  btn.pack()

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

def winCheck(itemPos):
  def moveAndCheck(moveAction):
    currentPos = itemPos
    connectCount = 0
    for i in range(1, 4):
      currentPos = moveAction(currentPos)
      if currentPos['column'] >= 0 and currentPos['column'] < gridColumns and currentPos['row'] >= 0 and currentPos['row'] < gridRows and \
      grid[currentPos['column']][currentPos['row']]['state'] == currentPlayer:
         connectCount += 1
    return True if connectCount == 3 else False
  
  left = moveAndCheck(lambda pos: {'column': pos['column']-1, 'row': pos['row']} )
  right = moveAndCheck(lambda pos: {'column': pos['column']+1, 'row': pos['row']} )
  down = moveAndCheck(lambda pos: {'column': pos['column'], 'row': pos['row']-1} )
  dLeft = moveAndCheck(lambda pos: {'column': pos['column']-1, 'row': pos['row']-1})
  dRight = moveAndCheck(lambda pos: {'column': pos['column']+1, 'row': pos['row']-1})
  if left or right or down or dLeft or dRight: 
    win()
  else: nextStep()

def onclick(event):
  item = event.widget.find_closest(event.x, event.y)[0]
  itemPos = findItemInGrid(item) 

  if itemPos is not None:
    nxt = False
    rowCount = -1
    for row in grid[itemPos['column']]:
      rowCount += 1

      if row['state'] == State.EMPTY:
        row['state'] = currentPlayer
        if currentPlayer == State.PLAYER1: canvas.itemconfig(row['id'], fill=status['color1'])
        else: canvas.itemconfig(row['id'], fill=status['color2'])
        nxt = True
        itemPos['row'] = rowCount
        break
    if nxt: winCheck(itemPos)

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
popupWindow = None

width = 600
height = 550
draw_offset = 5
circle_size = 70

currentPlayer = State.PLAYER1
status = {'text1': "Current player: ", 'text2': "Player 1", 'color1': "#F00", 'color2': "#FF0"}

canvas = init_canvas()
statusTextItem = canvas.create_text(draw_offset * 2, height - 50 + draw_offset, text=(status['text1'] + status['text2']), anchor=NW)
canvas.create_text(draw_offset * 2, height - 25 + draw_offset, text="Player colour:", anchor=NW)
statusColorItem = canvas.create_oval(draw_offset * 2 + 105, height - 25 + draw_offset, draw_offset * 2 + 105 + 15, height - 25 + draw_offset + 15, fill=status['color1'])
grid = draw_grid(canvas, width, height - 50, circle_size, draw_offset)

game.mainloop()
