import sys

import sys

def main () -> None:

    itxt = open("input.txt", mode='r').read().splitlines()
    itxt = [i.split() for i in itxt]

    x = 1
    clk = 0

    def incclk():
        nonlocal x, clk

        if (clk+1) % 40 == 0:
            print('\n', end='')
        elif clk%40 == x or clk%40 == x-1 or clk%40 == x+1:
            print('▓', end='')
        else:
            print('░', end='')
            
        clk += 1
        
        
    for ins in itxt:
        if ins[0] == 'noop':
            incclk()
        elif ins[0] == 'addx':
            incclk()
            incclk()
            x += int(ins[1]) 
            

if __name__ == '__main__':
    sys.exit(main()) 
