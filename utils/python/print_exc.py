# coding: utf-8
import sys, traceback

def print_exc_plus():
    """打印通常的回溯信息，且附有每帧中的局部变量的列表
    """

    tb = sys.exc_info()[2]
    while tb.tb_next:
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print 'Locals by frame, innermost last'
    for frame in stack:
        print
        print 'Frame %s in %s at line %s' %(frame.f_code.co_name, frame.f_code.co_filename, frame.f_lineno)

    for key, value in frame.f_locals.items():
        print '\t%20s = ' % key,
        # 我们必须_绝对_避免一场的扩散，而str(value)
        # _能够_引发任何异常，所以我们_必须_捕获所有异常
        try:
            print value
        except:
            print '<ERROR WHILE PRINTING VALUE>'


if __name__ == '__main__':
    try:
        test1 = str(test)
    except:
        traceback.print_exc()
        print '=========='
        print_exc_plus()
