with open('day6/input.txt', 'r') as f:
    elf_comms = f.read()

def findMarker(signal, marker_length):
   for i in range(len(signal)-(marker_length-1)):
    marker =  signal[i:i+marker_length]
    if len(set(marker)) == marker_length:
        return i+marker_length

print("Position of first marker:", findMarker(elf_comms, 4)) # part one
print("Position of first marker:", findMarker(elf_comms, 14)) # part two