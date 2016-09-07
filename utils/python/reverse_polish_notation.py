# -*- coding: utf8 -*-

'''
逆波兰相关的函数
'''

def evalRPN(tokens):
    '''
    Evaluate the value of an arithmetic expression in Reverse Polish Notation.

    >>> evalRPN(["2", "1", "+", "3", "*"])
    9
    >>> evalRPN(["4", "13", "5", "/", "+"])
    6
    >>> evalRPN(["18"])
    18
    >>> evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"])
    22
    '''
    import operator
    _operators = {'+': operator.add,
                  '-': operator.sub,
                  '*': operator.mul, 
                  '/': operator.div,
                 }
    stack = []

    for c in tokens:
        if c in _operators:
            stack.append(int(_operators[c](int(stack.pop(-2))*1.0, int(stack.pop()))))
        else:
            stack.append(c)

    return int(stack.pop())

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
