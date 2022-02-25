import mmap

with open('./controllerFiles/INFO.BIN', 'r+b') as file:
    mm = mmap.mmap(file.fileno(), 0)
    print(mm[int('1F', 16)])
    #print(file.readlines()) 

    # if this isnt the object dictionary then what the heck is