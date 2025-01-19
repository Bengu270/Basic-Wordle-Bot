# A simple wordle bot which will automatically solve WordleCup.io puzzles. 
# It automatically figures out the next word and enters it for you until it it wins or fails.
# Uses a basic linear search algorithm and conditionals to find the next matching word.
# Has a 5-word database in WordFile.txt: Currently contains 3317 words. This is not the full database for wordle.
# Bot is not 100% accurate and may fail in some cases (e.g. if the word is not in the database).
# Also currently only works on WordleCup.io and not the original Wordle game, but can be easily modified to do so.
# Created by: Bengu270

# Importing libraries
import pyautogui as gui, time
from PIL import Image
import keyboard

# Finds the 5x6 grid on screen using the WordleGrid.png image
def FindGrid():
    try:
        gridLocation = gui.locateOnScreen('WordleGrid.png')
        if gridLocation:
            gridLocationTuple = (
                int(gridLocation.left), 
                int(gridLocation.top), 
                int(gridLocation.width), 
                int(gridLocation.height)
            )
            print(gridLocationTuple)
            return gridLocationTuple
        else:
            return False
    except:
        print("Grid not on screen")

# Takes a screenshot of the grid at given coordinates
def GridScreenshot(gridLocation):
    image = gui.screenshot(region = gridLocation)
    image.save('GridScreenshot.png')

# Opens the WordFile.txt file and returns a list of words
def OpenWordFile():
    wordFile = open("WordFile.txt", "r")
    words = [line.strip() for line in wordFile]
    return words

# Returns the colour of a pixel at given coordinates
def PixColour(image_path, x, y):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        pixel_color = img.getpixel((x, y))
    return pixel_color

# Identifies the colour of a pixel and returns the colour. Only returns grey, green, yellow, or dark green (colours of wordle letters or end screen)
def FindColour(x):
    if str(x) == "(162, 162, 162)":
        colour = "grey"
    elif str(x) == "(87, 172, 120)":
        colour = "green"
    elif str(x) == "(233, 198, 1)":
        colour = "yellow"
    elif str(x) == "(0, 128, 0)":
        colour = "dark green"
    try:
        return colour
    except:
        print("Colour not identified")

# Enters a word into the Wordle game and presses enter
def EnterWord(currentWord):
    gui.write(currentWord)
    gui.press("enter")
    time.sleep(0.2)

# Appends the green, yellow, and grey lists with the current word and returns the updated lists. Lists store known green, yellow and grey letters.
def AppendWordLists(green, greenCount, yellow, yellowLocations, grey, currentWord, row):

    match row:
        case 1:
            row = 50
        case 2:
            row = 115
        case 3:
            row = 180
        case 4:
            row = 245
        case 5:
            row = 310
        
    currentWord = currentWord
    for i in range(5):
        colour = FindColour(PixColour("GridScreenshot.png", (50 + 65*i), row))
        if colour == "green":
            green[i] = currentWord[i]
            greenCount += 1
        elif colour == "yellow":
            yellow.append(currentWord[i])
            yellowLocations[i].append(currentWord[i])
        elif colour == "grey":
            grey.append(currentWord[i])
            for letter in grey[:]:
                if letter in green:
                    grey.remove(letter)
                elif letter in yellow:
                    grey.remove(letter)
        else:
            pass
    return green, greenCount, yellow, yellowLocations, grey, currentWord

# Filtering algorithm to find the next word to guess. Filters out words that don't contain yellow letters or green letters in the right space and letters in grey.
def WordFilter(words, green, yellow, yellowLocations, grey, currentWord):
    match = False
    wordCount = 0
    while match == False:
        checkedWord = words[wordCount]

        exit = False

        if yellow != False:
            for y in yellow:
                exit = True
                if y in checkedWord:
                    exit = False
                if exit == True:
                    break
            
        for i in range(5):
            if checkedWord[i] in yellowLocations[i]:
                exit = True
                break

        for i in range(5):
            if green[i] != "-":
                if checkedWord[i] != green[i]:
                    exit = True
                    break

            if checkedWord[i] in grey: 
                exit = True
                break
                
            if exit == True:
                break
        
        if checkedWord == currentWord:
            exit = True

        if exit == False:
            match = True
            return checkedWord
        else:
            wordCount+=1
            if wordCount == len(words)-1:
                print("Word not found in database")
                return

# Checks if the end screen is present
def CheckWin():
    if FindColour(PixColour("GridScreenshot.png", 152, 138)) == "dark green":
        return True
    else:
        return False

# Main function that runs the program
def main():
    words = OpenWordFile()
    green = ["-"]*5
    greenCount = 0
    yellow = []
    yellowLocations = [[],[],[],[],[]]
    grey = []
    currentWord = ""
    row = 0

    gridLocation = FindGrid()
    
    # Starts game with 3 opening words (adieu, thorn and clamp). It will hop out of the opening sequence if enough greens and yellows are found.

    currentWord = "adieu"
    EnterWord(currentWord)
    print(gridLocation)
    GridScreenshot(gridLocation)
    if GridScreenshot(gridLocation) == False:
        return
    if CheckWin():
        return
    row +=1
    green, greenCount, yellow, yellowLocations, grey, currentWord = AppendWordLists(green, greenCount, yellow, yellowLocations, grey, currentWord, row)
    print(green, greenCount, yellow, yellowLocations, grey, currentWord)

    if greenCount + len(yellow) <= 3 and greenCount<=2 and len(yellow)<= 3:
        currentWord = "thorn"
        EnterWord(currentWord)
        GridScreenshot(gridLocation)
        if CheckWin():
            return
        row +=1
        green, greenCount, yellow, yellowLocations, grey, currentWord = AppendWordLists(green, greenCount, yellow, yellowLocations, grey, currentWord, row)
        print(green, greenCount, yellow, yellowLocations, grey, currentWord)

    if greenCount + len(yellow) <= 3 and greenCount<=2 and len(yellow)<= 3:
        currentWord = "clamp"
        EnterWord(currentWord)
        GridScreenshot(gridLocation)
        if CheckWin():
            return
        row +=1
        green, greenCount, yellow, yellowLocations, grey, currentWord = AppendWordLists(green, greenCount, yellow, yellowLocations, grey, currentWord, row)
        print(green, greenCount, yellow, yellowLocations, grey, currentWord)

    currentWord = WordFilter(words, green, yellow, yellowLocations, grey, currentWord)
    
    EnterWord(currentWord)
    GridScreenshot(gridLocation)

    # Starts word filtering system. Will continue until end screen shows.
    while not CheckWin():
        row +=1
        green, greenCount, yellow, yellowLocations, grey, currentWord = AppendWordLists(green, greenCount, yellow, yellowLocations, grey, currentWord, row)
        print(green, greenCount, yellow, yellowLocations, grey, currentWord)

        currentWord = WordFilter(words, green, yellow, yellowLocations, grey, currentWord)
        if currentWord == None:
            return
        
        EnterWord(currentWord)
        GridScreenshot(gridLocation)
    
    return

if __name__ == "__main__":
    # Hotkey 'Shift' to start the program
    def onKey():
        main()
    
    keyboard.add_hotkey('shift', onKey)
    
    print("Click on the wordle grid and press 'shift' to solve. Press 'esc' to quit.")
    
    keyboard.wait('esc')


