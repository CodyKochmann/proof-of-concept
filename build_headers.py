# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-01 08:14:12
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-01 08:42:47

from setuptools.sandbox import pushd
import os

__file__path = os.path.dirname(os.path.abspath(__file__))

ls = lambda d='./': os.listdir(d)
neighbor_dirs = lambda: (i for i in ls() if os.path.isdir(i) and not i.startswith('.'))
target_markdowns = lambda: (i for i in ls() if os.path.isfile(i) and i.endswith('.md') and i.split('.')[0] in {'observation','experiment'})

with pushd(__file__path):
    for current_dir in neighbor_dirs():
        with pushd(current_dir):
            for target in target_markdowns():
                header = '## {} - {}\n'.format(
                    target.split('.')[0],
                    target.split('.')[1].replace('_', ' ')
                )
                file_content = ''
                with open(target, 'r') as f:
                    tmp = f.read()
                    if not tmp.startswith(header):
                        file_content = tmp
                if file_content:
                    print('writing header to', target)
                    with open(target, 'w') as f:
                        f.write('{}\n{}'.format(header, file_content))
