import tkinter     #GUI Library: windows, buttons, labels, text boxes, etc

button_values = [
    ["C", "B", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", "√", ".", "="],
]
top_values = ["C", "B", "%"]
right_values = ["÷", "×", "-", "+", "="]

row_count = len(button_values)     #returns no of button values
coloumn_count = len(button_values[0])    #returns no of columns using top row. eg-len(button_values[0]) (at index 0)

color_white = "#FFFFFF"
color_black = "#000000"
color_lightpink = "#ff6bb0"
color_darkpink = "#C51877"
color_pink = "#FF2579"

window = tkinter.Tk()     #create a window. Tk(): func/class
window.title("Calculator")
window.resizable = (False, False)

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text= "0", font= ("Arial", 45), background= color_black, foreground= color_white, anchor= "e", width= coloumn_count) #width= column_count > maximum width we want

label.grid(row= 0, column= 0, columnspan= coloumn_count, sticky= "we")     #Grid: starts from 0 for both row and column, putting label stretch from left to right on grid 0 (excel layout), i.e, label is in 0th row and 0th column stretching on column count , left to right. columnspan = how many columns label should take (on columns inside column_count) to take entire space. Sticky (stretch) west-east. 

for row in range(row_count):     #repeat for every row (eg- row count 4, so 0, 1, 2, 3)
    for column in range(coloumn_count):     #inside each row, go through each column (eg- column count 4, so 0, 1, 2, 3)
        value = button_values[row][column]
        button = tkinter.Button(frame, text= value, font= ("Arial", 25),
                                width= coloumn_count-1, height= 1,
                                background= color_darkpink, foreground= color_white, 
                                command= lambda value=value: button_clicked(value))     #cant use command= button_clicked(value) > cuz we have to create function when clicked, then run button_clicked (command needs a function not result of its execution). width = enough to have column_count-1 values, height = enough for 1 value (tkinter = size approximated by no of characters it can fit)
        
        if value in top_values:
            button.config(background= color_lightpink, foreground= color_black, font= ("Arial", 25), width= coloumn_count-1, height= 1)
        elif value in right_values:
            button.config(background= color_pink, foreground= color_black, font= ("Arial", 25), width= coloumn_count-1, height= 1)
        #else:
            #button.config(background= color_darkblue, foreground= color_white) #NOT NEEDED, ALREADY SPECIFIED

        button.grid(row = row + 1, column = column, sticky= "nsew")     #since grid starts from 0(occupied by label), button starts from grid 1. Column changes as row changes to affect diff buttons. sticky = nsew (fill entire space/all directions to fill boxes neatly)

frame.pack()

#Memory: A+B, A-B, AxB, A/B     [operand-operator-operand]
A = "0"     #A is 1st no, default value 0 (label display shows 0)
operator = None     #empty at start, chosen later
B = None

def clear_all():
    global A, operator, B
    A = "0"     #what we want the label to have when we click "C"
    operator = None
    B = None

def delete():
    current = label["text"]     #takes what is currently on label
    current = current[:-1]     #removes last digit
    if current:
        label["text"] = current     #if there is still smth in current > show it
    else:     #confirmed there is nothing in current
        label["text"] = "0"     #show 0

def remove_0_decimal(num):     #to not show '.0' after nos
    if num % 1 == 0:     #% = remainder (if remainder is 0 > in most case of %1)
        num = int(num)     #removes '.0' (eg- 0.5 > 5)
    return str(num)

def button_clicked(value):
    global top_values, right_values, A, operator, B #Global = can be any value in A & B, no local variables (accesses variables outside of function (outside def))

    if value in top_values:
        if value == "C":
            clear_all()
            label["text"] = "0"
        elif value == "B":
            delete()
        #elif value == "+/-":     #USE WHEN "+/-" BUTTON EXISTS
            #result = float(label["text"]) * -1
            #label["text"] = remove_0_decimal(result)
        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_0_decimal(result)

    elif value in right_values:
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]     #takes 2nd no as B (whatever on text label)
                numA = float(A)
                numB = float(B)
                if operator == "+":
                    label["text"] = remove_0_decimal(numA + numB)
                elif operator == "-":
                    label["text"] = remove_0_decimal(numA - numB)
                elif operator == "×":
                    label["text"] = remove_0_decimal(numA * numB)
                elif operator == "÷":
                    label["text"] = remove_0_decimal(numA / numB)
                clear_all()
        elif value in "+-×÷":
            if operator is None:     #If the user presses an operator (+, −, ×, ÷), the code saves the first number (A), resets the screen to 0, and remembers the operator for the next step.
                A = label["text"]
                label["text"] = "0"
                B = "0"
            operator = value

    else:
        if value == ".":
            if value not in label["text"]:
                label["text"] += value     #if theres no '.' in label, only then we can add it (add to existing value), otherwise do nothing
        elif value == "√":
            num = float(label["text"])     #(eg- after float 9 > 9.0)
            label["text"] = remove_0_decimal(num ** 0.5)     #** > power/exponent, 0.5 > half, str > turns num into smth we can show on screen
        elif value in "0123456789":     #use 'in', not == (comparison) since we would wanna know if 1 in "0123456789", not 1 == "0123456789" which is obviously false.
            pass
            if label["text"] == "0":     #we dont want first digit 0 (eg- 05, insted we want 5) [REPLACES DEFAULT 0]
                label["text"] = value     #replace 0 (use '=' (assign), not '==' (comparison))
            else:
                label["text"] += value     #add & assign(append) i.e add value to end of current text

#shift window to open in the center
window.update()
window_width = window.winfo_width()     # returns current size of window (winfo = window info)
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()     #returns size of user screen
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))     #(half of screen)-(half of window width) > how far from left of screen
window_y = int((screen_height/2) - (window_height/2))     #(half of screen)-(half of window height) > how far from top of screen
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")     #format= (width)x(height)+(x)+(y) no spcaes allowed

window.mainloop()     #keeps window stay alive & not close immediately