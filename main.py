# TB TODO - List possible words based on the intersection of across + down instead of just one facing
# TB TODO - Try filling out multiple lines automatically
from blessed import Terminal
import puz
import sys
import re

term = Terminal()
#print( 'I am ' + term.underline + 'bold' + term.normal + '!' )

puz_data = puz.Puzzle()
"""
crossword_size = (15,15)
crossword_data = []
for row in range(crossword_size[1]):
    s = ''.join( ['x' for _ in range(crossword_size[0])])
    crossword_data.append(s)
#crossword_data = ['ABCDEFG', 'HIJKLMM', 'NOPQRSS', 'TUVWXYZ', 'ABCDEFG', 'HIJKLM', 'NOPQRS' ]
"""

DRAW_CROSSWORD_START = (2,2)
across_word_starts = {}
down_word_starts = {}
big_word_list = {}
big_words = ""

# needle = "ABC  XT" where space is missing letter that could be anything
def find_matching_words(needle):
    MAX_SUGGESTIONS = 20

    # Current word could be none if you're located on a black square
    if needle is None:
        return []

    builder = []
    for c in needle:
        if c == ' ':
            builder.append('[A-Z0-9]')
        else:
            builder.append(c)
    builder.append(';[0-9]+')
    reg = ''.join(builder)

    #reg = r"ANGELI[A-Z];[0-9]+"
    #reg = r"OPEN[A-Z][A-Z][A-Z][A-Z];[0-9]+"
    all_matches = re.findall(reg, big_words)
    result = []
    for a in all_matches:
        word, score = a.split(';')
        result.append((word,int(score)))
    result.sort(key=lambda x: -x[1])

    if len(result) > MAX_SUGGESTIONS: 
        result = result[:MAX_SUGGESTIONS]
        result.append(('(more)',0))
    return result


# TB TODO - Would be nice to load async
def load_big_word_list():
    """
    with open('words.txt') as f:
        for line in f.read().splitlines():
            # print(line)
            word, score = line.split(';')
            if len(word) not in big_word_list:
                big_word_list[len(word)] = []
            big_word_list[len(word)].append((word,score))
    print(len(big_word_list))
    exit()
    """
    # Faster to just do a regex on everything?
    # Could still separate it by word length, but just do a big chunk of data
    global big_words
    with open('words.txt') as f:
        big_words = f.read()
    # find_matching_words('ANGELI ')

def find_word_starts():
    across_word_starts.clear()
    down_word_starts.clear()

    for y in range(puz_data.height):
        word_x = 0
        for x in range(puz_data.width):
            if puz_data.solution[ y*puz_data.width + x ] == '.':
                word_x = x+1
                across_word_starts[(x,y)] = None
            else:
                across_word_starts[(x,y)] = word_x

    for x in range(puz_data.width):
        word_y = 0
        for y in range(puz_data.height):
            if puz_data.solution[ y*puz_data.width + x ] == '.':
                word_y = y+1
                down_word_starts[(x,y)] = None
            else:
                down_word_starts[(x,y)] = word_y


def print_word_suggestions( current_word ):
    x = DRAW_CROSSWORD_START[0] + puz_data.width * 4 + 5
    y = DRAW_CROSSWORD_START[1]
    print(term.blue_on_black)
    #print(term.move_xy(x,y), end='') 
    #print(current_word, end='')
    #print('wtfffffff', end='')
    for sugg in find_matching_words(current_word):
        print(term.move_xy(x,y), end='') 
        print(f"{sugg[0]}     {sugg[1]}", end='')
        y+=1

def update_cursor(pos):
    x = pos[0]*4 + DRAW_CROSSWORD_START[0] + 2
    y = pos[1]*2 + DRAW_CROSSWORD_START[1] + 1
    print(term.move_xy(x,y), end='')
    print('', end='', flush=True)

def print_crossword():
    print(term.green_on_black)
    for row in range(puz_data.height):
        #print('┌─ ┬ ┐')
        print(term.move_xy(DRAW_CROSSWORD_START[0], DRAW_CROSSWORD_START[1]+(row*2)), end='') 
        for col in range(puz_data.width):
            if col == 0:
                if row == 0:
                    print('┌───', end='')
                else:
                    print('├───', end='')
            elif col == puz_data.width-1:
                if row == 0:
                    print('┬───┐', end='')
                else:
                    print('┼───┤', end='') 
            else:
                if row == 0:
                    print('┬───', end='')
                else:
                    print('┼───', end='')

        print(term.move_xy(DRAW_CROSSWORD_START[0], DRAW_CROSSWORD_START[1]+(row*2)+1), end='') 
        for col in range(puz_data.width):
            print('│', end='')
            datapos = row*puz_data.width + col
            ch = puz_data.solution[datapos]
            if ch == '.':
                ch = '█'
            print(' ' + ch + ' ', end='')
        print('│', end='')

    print(term.move_xy(DRAW_CROSSWORD_START[0], DRAW_CROSSWORD_START[1]+(puz_data.height*2)+2-2), end='') 
    for col in range(puz_data.width):
        if col == 0:
            print('└───', end='')
        elif col == puz_data.width-1:
            print('┴───┘', end='')
        else:
            print('┴───', end='')

def print_box(x,y,color):
    print(color)

    # Top row
    print(term.move_xy(DRAW_CROSSWORD_START[0]+(x*4), DRAW_CROSSWORD_START[1]+(y*2)), end='') 
    if x == 0:
        if y == 0:
            print('┌───┬', end='')
        else:
            print('├───┼', end='')
    elif x == puz_data.width-1:
        if y == 0:
            print('┬───┐', end='')
        else:
            print('┼───┤', end='')
    else:
        if y == 0:
            print('┬───┬', end='')
        else:
            print('┼───┼', end='')

    # Middle row
    print(term.move_xy(DRAW_CROSSWORD_START[0]+(x*4), DRAW_CROSSWORD_START[1]+(y*2)+1), end='') 
    print('│')
    print(term.move_xy(DRAW_CROSSWORD_START[0]+(x*4)+4, DRAW_CROSSWORD_START[1]+(y*2)+1), end='') 
    print('│')

    # Bottom row
    print(term.move_xy(DRAW_CROSSWORD_START[0]+(x*4), DRAW_CROSSWORD_START[1]+(y*2)+2), end='') 
    if x == 0:
        if y == puz_data.height - 1:
            print('└───┴', end='')
        else:
            print('├───┼', end='')
    elif x == puz_data.width-1:
        if y == puz_data.height - 1:
            print('┴───┘', end='')
        else:
            print('┼───┤', end='')
    else:
        if y == puz_data.height - 1:
            print('┴───┴', end='')
        else:
            print('┼───┼', end='')




def print_facing(pos,facing,color):
    #print_box(x,y,color)
    #update_cursor(pos)

    ch = puz_data.solution[pos[1]*puz_data.height + pos[0]]
    if ch == '.':
        print_box(pos[0],pos[1],color)
        update_cursor(pos)
        return

    if facing == FACING_ACROSS: 
        for x in range( across_word_starts[pos], puz_data.width ):
            ch = puz_data.solution[pos[1]*puz_data.height + x]
            if ch == '.':
                break
            else:
                print_box(x,pos[1],color)

    elif facing == FACING_DOWN:
        for y in range( down_word_starts[pos], puz_data.height ):
            ch = puz_data.solution[y*puz_data.height + pos[0]]
            if ch == '.':
                break
            else:
                print_box(pos[0],y,color)

def get_current_word(pos,facing):
    ch = puz_data.solution[pos[1]*puz_data.height + pos[0]]
    if ch == '.':
        return None

    word_builder = []
    if facing == FACING_ACROSS: 
        for x in range( across_word_starts[pos], puz_data.width ):
            ch = puz_data.solution[pos[1]*puz_data.height + x]
            if ch == '.':
                break
            else:
                word_builder.append(ch)

    elif facing == FACING_DOWN:
        for y in range( down_word_starts[pos], puz_data.height ):
            ch = puz_data.solution[y*puz_data.height + pos[0]]
            if ch == '.':
                break
            else:
                word_builder.append(ch)

    result = ''.join(word_builder)
    return(result)



def print_title(pos):
    print(term.home + term.clear)
    print(term.green_on_black)
    # print(f"{term.home}{term.green_on_black}{term.clear}")
    print(f"{term.black_on_blue}")
    with term.location(0,0):
        print(f" CROSSWORD {pos[0]},{pos[1]}", end='')
    with term.location(0,term.height-1):
        print(f" BOTTOM {pos[0]},{pos[1]}", end='')

def print_everything(pos):
    print_title(pos)
    print_crossword()
    update_cursor(pos)


#print(f"{term.home}{term.black_on_skyblue}{term.clear}")
#print(term.height)
#print("press 'q' to quit.")
FACING_ACROSS = 0
FACING_DOWN = 1
def go():
    pos = (0,0)
    facing = FACING_ACROSS
    print_everything(pos)
    print_facing(pos, facing, term.white_on_black)
    with term.cbreak():
        val = ''
        while val.lower() != 'q':
            # print_everything()
            update_cursor(pos)
            val = term.inkey(timeout=3)
            if not val:
                # print("It sure is quiet in here ...")
                pass
            elif val.is_sequence:
                # print("got sequence: {0}.".format((str(val), val.name, val.code)))
                # TB TODO - Only redraw the facing if something changed
                old_pos = pos
                old_facing = facing
                redraw_facing = False
                if val.code == term.KEY_LEFT:
                    if facing == FACING_DOWN:
                        facing = FACING_ACROSS
                        redraw_facing = True
                    else:
                        pos = (max(pos[0]-1,0), pos[1])
                        if across_word_starts[old_pos] != across_word_starts[pos]:
                            redraw_facing = True

                elif val.code == term.KEY_RIGHT:
                    if facing == FACING_DOWN:
                        facing = FACING_ACROSS
                        redraw_facing = True
                    else:
                        pos = (min(pos[0]+1,puz_data.width-1), pos[1])
                        if across_word_starts[old_pos] != across_word_starts[pos]:
                            redraw_facing = True
                elif val.code == term.KEY_DOWN:
                    if facing == FACING_ACROSS:
                        facing = FACING_DOWN
                        redraw_facing = True
                    else:
                        pos = (pos[0], min(pos[1]+1,puz_data.height-1))
                        if down_word_starts[old_pos] != down_word_starts[pos]:
                            redraw_facing = True
                elif val.code == term.KEY_UP:
                    if facing == FACING_ACROSS:
                        facing = FACING_DOWN
                        redraw_facing = True
                    else:
                        pos = (pos[0], max(pos[1]-1,0) )
                        if down_word_starts[old_pos] != down_word_starts[pos]:
                            redraw_facing = True

                if redraw_facing:
                    print_facing(old_pos, old_facing, term.green_on_black)
                    print_facing(pos, facing, term.white_on_black)
                    print_word_suggestions( get_current_word(pos,facing) )

            elif val:
                # print("got {0}.".format(val))
                #puz_data.solution[pos[1]*puz_data.width + pos[0]] = val
                val = val.upper()
                new_index = pos[1]*puz_data.width + pos[0]
                puz_data.solution = puz_data.solution[:new_index] + val + puz_data.solution[new_index+1:]
                # print_crossword() 
                print(term.move_xy(DRAW_CROSSWORD_START[0] + pos[0]*4 + 2, DRAW_CROSSWORD_START[1]+ (pos[1]*2) +1), end='')
                print(val, end='')
                print_word_suggestions( get_current_word(pos,facing) )
        print(f'bye!{term.normal}')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        puz_data = puz.read(sys.argv[1])
    else:
        puz_data = puz.read('Jan1821.puz')
    find_word_starts() 
    load_big_word_list()
    go()
