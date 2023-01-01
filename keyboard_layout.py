import json
import pcbnew

FILE = "keyboard-layout.json"
#exec(open('keyboard_layout.py').read())

with open(FILE, "r") as f:
    kle = json.load(f)

#initial
xoff = 19.05 / 2.0
y = 19.05 / 2.0

x = xoff
xstep = 19.05
ystep = 19.05
k = 1

board = pcbnew.GetBoard()
footprints = board.GetFootprints()

xspc = 0

c_row = 0
for row in kle:
    print('-----------row------------')
    col = 0
    for f in row:
        if type(f) is str:
            coord = (int(x*1000000), int(x*1000000))
            print(f"SW{k}", coord)

            sw = board.FindFootprintByReference(f"SW{k}")
            sw.SetPosition(pcbnew.wxPointMM(x, y))

            # diode stuff
            d = board.FindFootprintByReference(f"D{k}")

            if c_row == 4: spc = -1
            elif c_row == 0: spc = 1
            else: spc = 0

            if col % 2 == 0:
                d.SetPosition(pcbnew.wxPointMM(x+xspc+(19.05/2.0)-1.6, y+spc))
            else:
                d.SetPosition(pcbnew.wxPointMM(x-xspc-(19.05/2.0)+1.6, y+spc))
            d.SetOrientationDegrees(90)
            x += xstep + xspc
            k += 1
            xspc = 0
            col += 1
        else:
            if 'y' in f:
                y += (float(f['y']) * ystep)
            if 'x' in f:
                x += (float(f['x']) * xstep)
            if 'w' in f:
                x += xstep * (float(f['w'] - 1)/2)
                xspc = xstep * (float(f['w'] - 1)/2)
    y += ystep
    c_row += 1
    x = xoff

pcbnew.Refresh()
