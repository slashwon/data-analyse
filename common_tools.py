# -*- coding: utf-8 -*-
import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def contain_zh(word):
    """
    判断字符串中是否包含中文字符
    """
    return re.match(zh_pattern, word)
