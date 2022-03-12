
# balanced parentheses in an expression
opening_brackets = ["[","{","("]
closing_brackets = ["]","}",")"]

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, char):
        self.stack.append(char)

    def pop(self):
        return self.stack.pop()

    def isEmpty(self):
        return len(self.stack)

    def top(self):
        return self.stack[-1]


# Main code
string = input('Enter string: ')

stack = Stack()   #creation of stack
balanced = True
# parcing through every character of the input
for char in string:
    # if the character is ( or [ or {, we push it to the stack until we find it's pair
    if char in opening_brackets: 
        stack.push(char)
    else:
        if stack.isEmpty() != 0:
            top = stack.top() #fetch the opening bracket from stack
            stack.pop() # and clear stack

            if char in closing_brackets:
                index = closing_brackets.index(char)
                if opening_brackets[index] != top: # same index means counterpart bracket (  (-->)  [-->] {-->} )
                    balanced = False
                    break
        else: # if stack is empty we don't have any opening bracket, so the string is unbalanced
            balanced = False
            break
#If stack is not empty after traversal then not balanced
if stack.isEmpty() != 0:
    balanced = False
if balanced:
    print("string is balanced!")
else:
    print("string is not balanced")