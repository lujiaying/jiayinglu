#-*- coding: utf-8 -*-

"""
A multiprocessing parallel framwork for data process
Author: Jiaying.lu
Date: 2017/09/07
"""

import os
import sys
import multiprocessing

def do_split_file(input_file, process_num):
    input_file_dir = os.path.dirname(os.path.abspath(input_file))
    split_file_dir = input_file_dir + '/split'
    if not os.path.exists(split_file_dir):
        os.mkdir(split_file_dir)
    split_prefix = split_file_dir + '/' + os.path.basename(input_file) + '.'

    cmd = 'rm %s/*' % (split_file_dir)
    ret = os.system(cmd)
    cmd = 'wc -l %s' % (input_file)
    ret = os.popen(cmd, 'r').read()
    line_file = int(ret.strip().split(' ')[0])
    line_split = int(round(line_file/process_num + 0.5))
    cmd = 'split -l %s -d -a 3 %s %s' % (line_split, input_file, split_prefix)
    ret = os.system(cmd)
    if ret != 0:
        sys.stderr.write('%s error\n' % (cmd))
        sys.exit(1)
    return [split_file_dir+'/'+_ for _ in os.listdir(split_file_dir)]

def test_func(input_file, output_file, seperator, stopwords_set):
    print 'enter _test_func, %s, %s, %s, %s' % (input_file, output_file, seperator, stopwords_set)
    with open(input_file) as fopen, open(output_file, 'w') as fwrite:
        for line in fopen:
            line_list = line.strip().split(seperator)
            res = filter(lambda _: not _ in stopwords_set, line_list)
            fwrite.write('%s\n' % (seperator.join(res)))

def merge_output_file(output_split_list, output_file):
    cmd = 'cat '
    for _ in output_split_list:
        cmd += (_ + ' ')
    cmd += ('> ' + output_file)
    cmd_re = os.system(cmd)
    if cmd_re != 0:
        sys.stderr.write('cmd:%s returns %s' % (cmd, cmd_re))

def do_parallel(input_file, output_file, process_num, func, *args):
    print args
    # split input file
    split_file_list = do_split_file(input_file, process_num)
    
    # Use process pool to execute func
    output_file_list = []
    pool = multiprocessing.Pool(processes = process_num)
    try:
        for split_file_path in split_file_list:
            output_file_path = split_file_path + '.out'
            output_file_list.append(output_file_path)
            func_args = [split_file_path, output_file_path] + list(args)
            pool.apply_async(func, tuple(func_args))
    except KeyboardInterrupt:
        sys.stderr.write('Caught KeyboardInterrupt, terminating workers\n')
        pool.terminate()
    else:
        pool.close()
    pool.join()

    # Merge ouput
    merge_output_file(output_file_list, output_file)

if __name__ == '__main__':
    do_parallel('./data/input', './output/test', 6, test_func, ' ', set(['aaabbb']))
