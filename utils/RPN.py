# -*- coding: utf8 -*-

'''
逆波兰相关
'''

def evalRPN(tokens):
    '''
    Evaluate the value of an arithmetic expression in Reverse Polish Notation.
    
    Usage:
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
    _stack = []

    for c in tokens:
        #print(_stack)
        if c in _operators:
            _stack.append(int(_operators[c](int(_stack.pop(-2))*1.0, int(_stack.pop()))))
        else:
            _stack.append(c)

    return int(_stack.pop())

def IN2RPN(tokens):
    '''
    Transfrom infix notation to reverse polish notation.
    
    Usage:
    >>> IN2RPN(['(', '2', '+', '1', ')', '*', '3'])
    ['2', '1', '+', '3', '*']
    >>> IN2RPN(['4', '+', '13', '/', '5'])
    ['4', '13', '5', '/', '+']
    >>> IN2RPN(['10', '*', '(', '6', '/', '(', '(', '9', '+', '3', ')', '*', '-11', ')', ')', '+', '17', '+', '5'])
    ['10', '6', '9', '3', '+', '-11', '*', '/', '*', '17', '+', '5', '+']
    '''

    _operators = {'+':1, '-':1, '*':2, '/':2}    # operators with weights
    _stack = []
    result = []

    for c in tokens:
        # print c, _stack, result
        if c == ')':
            result.append(_stack.pop())
            _stack.pop()
        elif c == '(':
            _stack.append(c)
        elif c in _operators:
            if not _stack or _stack[-1] == '(':
                _stack.append(c)
            elif _operators[c] > _operators[_stack[-1]]:
                _stack.append(c)
            else:
                result.append(_stack.pop())
                _stack.append(c)
        else:
            result.append(c)

    while _stack:
        result.append(_stack.pop())
    return result

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
