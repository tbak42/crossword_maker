from blessed import Terminal

term = Terminal()
print( 'I am ' + term.underline + 'bold' + term.normal + '!' )

DRAW_CROSSWORD_START = (2,2)
def print_crossword():
    print(term.green_on_black)
    for row in range(crossword_size[1]):
        print(term.move_xy(DRAW_CROSSWORD_START[0], DRAW_CROSSWORD_START[1]+row), end='')
        print("ABCDEFBEFS", end='')
    print(term.move_xy(pos[0]+DRAW_CROSSWORD_START[0], pos[1]+DRAW_CROSSWORD_START[1]), end='')
    #print(term.move_xy(2,2))
    print('X', end='', flush=True)

def print_title():
    print(term.home + term.clear)
    print(term.green_on_black)
    # print(f"{term.home}{term.green_on_black}{term.clear}")
    print(f"{term.black_on_blue}")
    with term.location(0,0):
        print(f" CROSSWORD {pos[0]},{pos[1]}")
    with term.location(0,term.height-1):
        print(f" BOTTOM {pos[0]},{pos[1]}")

def print_everything():
    print_title()
    print_crossword()

pos = (0,0)
crossword_size = (5,5)

print(f"{term.home}{term.black_on_skyblue}{term.clear}")
print(term.height)
print("press 'q' to quit.")
with term.cbreak():
    val = ''
    while val.lower() != 'q':
        print_everything()
        val = term.inkey(timeout=3)
        if not val:
            # print("It sure is quiet in here ...")
            pass
        elif val.is_sequence:
            # print("got sequence: {0}.".format((str(val), val.name, val.code)))
            if val.code == term.KEY_LEFT:
                pos = (max(pos[0]-1,0), pos[1])
            elif val.code == term.KEY_RIGHT:
                pos = (min(pos[0]+1,crossword_size[0]-1), pos[1])
            elif val.code == term.KEY_DOWN:
                pos = (pos[0], min(pos[1]+1,crossword_size[1]-1))
            elif val.code == term.KEY_UP:
                pos = (pos[0], max(pos[1]-1,0) )

        elif val:
            # print("got {0}.".format(val))
            pass
    print(f'bye!{term.normal}')