#coding: utf-8
import hashlib

def generate_signature(**kwargs):
    """
    @brief 根据给定的key，生成加密签名

    @para **kwargs = {'install_id':.., 'random_para_name':random_para_key, 'random_para_key':.., 'version':.., 'platform':..}
    @return signature.hexdigest(): 十六进制表示的加密签名
    """

    signature = ''

    # 1.将user_id 和 kwargs中的key进行字典序排序，
    # 2.将三个参数字符串拼接成一个字符串进行md5加密
    sorted_keys = kwargs.keys()
    sorted_keys.sort()
    concat_str = ''.join(map(lambda k:kwargs[k], sorted_keys))
    signature = hashlib.md5(concat_str)

    return signature.hexdigest()

def check_signature(**kwargs):
    """
    @brief 根据传入的字典，验证签名是否正确 

    @para **kwargs = {'install_id':.., 'random_para_name':random_para_key, 'random_para_key':.., 'version':.., 'platform':.., 'signature':..}
    @return True or False

    @test script:
    >>> check_signature(**{'install_id': '1422040116327028', 'random_para_name': 'uKRJTFwvg', 'uKRJTFwvg': 'gWqqk14Wb4CPr8HCpCFPUh', 'version': '1.7.0126', 'platform': 'a', 'signature':'9e121051771b86e8c828916e84538788'})
    True
    """

    signature_para_dict = dict(kwargs)
    signature = signature_para_dict.pop('signature')
    if signature == generate_signature(**signature_para_dict):
        return True
    else:
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()  #Doctest: documentation and unit-testing at the same time
