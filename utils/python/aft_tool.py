#-*- coding: utf-8 -*-
"""一个公用的工具类"""

import logging
import Image
import random
import time
import json
import sys,os,hashlib,base64
import urllib2
from urllib import quote
from urllib import urlencode 
from urllib import unquote 
from time import gmtime

logger = logging.getLogger('afanti')

def generate_thumbnail(input_image_path, thumbnail_path, thumbnail_height, thumbnail_width):
    """生成缩略图"""
    logger.debug("start to generate thumbnail, input image path :%s" % input_image_path)
    img = Image.open(input_image_path)
    hw_ratio = thumbnail_height * 1.0 / thumbnail_width
    img_width = img.size[0]
    img_height = img.size[1]
    img_hw = img_height * 1.0 / img_width
    if hw_ratio > img_hw:
        img.thumbnail((thumbnail_width, thumbnail_width * 1.0 / img_width * img_height))
    else:
        img.thumbnail((thumbnail_height * 1.0 / img_height * img_width, thumbnail_height))
    img.save(thumbnail_path)
    logger.debug("generate thumbnail success")


def store_file(memory_file, store_path):
    """
    @brief 内存文件存储

    @param [in] memory_file 内存文件
    @param [in] store_path 存储路径

    """
    logger.debug("start to store memory file %s to disk %s" % (memory_file, store_path))
    file_writer = open(store_path, 'w')
    for chunck in memory_file.chunks():
        file_writer.write(chunck)
    file_writer.close()
    logger.debug("store finish")

def generate_random_code(bit_num = 4):
    """
    @brief 生成随机字符串
    
    @param [in] bit_num 生成的随机字符串的位数

    @return 返回一串随机生成的字符串
    """
    random_number_list = random.sample([i for i in xrange(10)], bit_num)
    return ''.join(map(lambda x:str(x), random_number_list))


def form_time_string(time_int):
    """
    @brief 把int型的时间转换为string类型的时间
 
    @detail 具体的转换规则
       1分钟以内， 返回 “刚刚”  
       1分钟以上1小时以内， 返回“多少分钟前，向下取整”   
       1小时以上24小时以内，返回“多少小时前，向下取整”
       24小时到48小时，返回“昨天”
       48小时到72小时，返回“前天”
       72小时以前，返回“具体时间”
 
    @param [in] time_int 精确到秒的整型时间
 
    @return string类型的时间
 
    """
 
    current_time = int(time.time())
    diff = current_time - time_int
    if diff < 60:
        return "刚刚"

    if diff < 3600:
        return "%d分钟前" % int(diff/60)

    if diff < 3600 * 24:
        return "%d小时前" % int(diff/3600) 

    if diff < 3600 * 48:
        return "昨天"

    if diff < 3600 * 72:
        return "前天"

    if diff < 3600 * 24 * 30:
        return "%d天前" % int(diff/(3600 * 24))

    return time.strftime('%Y-%m-%d', time.localtime(time_int))
    
     
def get_age_from_birth_date(birth_date):
    """
    @brief 根据用户的出生日期计算其年龄

    @param [in] brith_date 是一个int值

    @return 年龄，周岁
    """
    birth_date = int(birth_date)
    birth_year = birth_date/10000
    birth_month = (birth_date % 10000) / 100
    birth_day = birth_date % 100

    current_time = gmtime()

    day_diff = current_time[2] - birth_day
    month_diff = current_time[1] - birth_month
    year_diff = current_time[0] - birth_year

    if day_diff < 0:
        month_diff = month_diff - 1
    if month_diff < 0:
        year_diff = year_diff - 1
    return year_diff

def get_constellation_from_birth_date(birth_date):
    """
    @brief 根据用户的出生日期获取星座

    @param [in] birth_date int值表示的是用户的出生年月日

    @return 返回的是星座
    """
    birth_date = int(birth_date)
    month_day = birth_date % 10000
    if month_day < 121:
        return "摩羯座"
    elif month_day < 220:
        return "水瓶座"
    elif month_day < 321:
        return "双鱼座"
    elif month_day < 421:
        return "白羊座"
    elif month_day < 522:
        return "金牛座"
    elif month_day < 622:
        return "双子座"
    elif month_day < 723:
        return "巨蟹座"
    elif month_day < 823:
        return "狮子座"
    elif month_day < 923:
        return "处女座"
    elif month_day < 1024:
        return "天秤座"
    elif month_day < 1123:
        return "天蝎座"
    elif month_day < 1222:
        return "射手座"
    else:
        return "摩羯座"


def rc4_func(string, op = 'encode', public_key = 'afanti_shared'):
    ckey_lenth = 4
    public_key = public_key and public_key or ''
    key = hashlib.md5(public_key).hexdigest()
    keya = hashlib.md5(key[0:16]).hexdigest()
    keyb = hashlib.md5(key[16:32]).hexdigest()
    keyc = ckey_lenth and (op == 'decode' and string[0:ckey_lenth] or hashlib.md5(str(time.time())).hexdigest()[32 - ckey_lenth:32]) or ''
    cryptkey = keya + hashlib.md5(keya + keyc).hexdigest()
    key_lenth = len(cryptkey)
    string = op == 'decode' and base64.urlsafe_b64decode(string[4:]) or '0000000000' + hashlib.md5(string + keyb).hexdigest()[0:16] + string
    string_lenth = len(string)

    result = ''
    box = list(range(256))
    randkey = []

    for i in xrange(255):
        randkey.append(ord(cryptkey[i % key_lenth]))

    for i in xrange(255):
        j = 0
        j = (j + box[i] + randkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp

    for i in xrange(string_lenth):
        a = j = 0
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))

    if op == 'decode':
        if (result[0:10] == '0000000000' or int(result[0:10]) - int(time.time()) > 0) and result[10:26] == hashlib.md5(result[26:] + keyb).hexdigest()[0:16]:
            return result[26:]
        else:
            return None
    else:
        return keyc + base64.urlsafe_b64encode(result)

def get_location(lng, lat):
    """
    @brief 获取位置信息
    
    @param [in] lng经度
    @param [in] lat纬度

    @return [location_datail_json, provice, city, city_code]
    """
    try:
        logger.debug("enter get loaction, [lng=%s, lat=%s]" % (lng, lat))
        baidu_request_url = "http://api.map.baidu.com/geocoder/v2/?ak=A49f0aad31ef721b8532b94b5e660673&location=%s,%s&output=json&pois=0" % (str(lng), str(lat))
        req = urllib2.Request(url=baidu_request_url)
        result_json = json.loads(urllib2.urlopen(req).read())
        if not result_json["status"] == 0:
            return ["", "", "", 0]
        location_detail = result_json["result"]
        province = location_detail["addressComponent"]["province"]
        city = location_detail["addressComponent"]["city"]
        city_code = int(location_detail["cityCode"])
        return [location_detail, province, city, city_code]
    except Exception, e:
        logger.error("error occurs during get location, error is:%s" % str(e))
        return ["", "", "", 0]

def rc4_encode(pure_string):
    added_num = len("1051412600") - len(pure_string)
    for i in range(0, added_num):
        pure_string += "#"
    encoded_result = rc4_func(pure_string)
    return urlencode({'': encoded_result})[1:]

def rc4_decode(encoded_string):
    
    return rc4_func(quote(encoded_string), 'decode').replace("#", "")
   

ul2d = lambda ids, names: map(lambda id,name:{'user_id':id,'user_name':name}, ids, names)

if __name__ == "__main__":

    print rc4_decode(rc4_encode(str(39365113)))
#    print rc4_decode("39edBfepHvgD%2Bfn5%2Bfn7qvr5%2Ba39%2Fq%2F5%2F%2Fz%2Br%2F3x%2BPj7%2FPv%2F")
#    print rc4_decode("39edBfepHvgD+fn5+fn7qvr5+a39/q/5/z+r/3x+Pj7/Pv/")
#    print rc4_decode("39edBfepHvgD+fn5+fn7qvr5+a39/q/5/z+r/3x+Pj7/Pv")
#    print get_constellation_from_birth_date(19871126)
#    for i in range(10000, 20000):
#        print i
#        a = rc4_encode(str(i))
#        print a
#        print rc4_decode(a)
#    time.sleep(10)
#    print rc4_encode(a, 'decode')
#    print rc4_encode("10978600")
#    result = get_location(39.983424,116.322987)
#    for key in result:
#        print key
    
 
