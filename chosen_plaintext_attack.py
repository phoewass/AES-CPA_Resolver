 #! /bin/python
import requests
from lxml import html

def hex_array(hex_str):
    return [l+h for l,h in zip(hex_str[0::2], hex_str[1::2])]

def get_page_content(data=None):
    url = 'https://aescpa.herokuapp.com/'
    res = requests.get(url, params={'data':data})
    return html.fromstring(res.content)

def get_encrypted_secret():
    page = get_page_content()
    return page.xpath('//p[@class="secret"]/text()')[0].__str__().strip()

def get_ciphertext(plaintext):
    page = get_page_content(plaintext)
    output = page.xpath('//div[@class="row"]//div[@class="col-lg-8 col-lg-offset-2"]//td[last()]/text()')
    return output[1].__str__().strip()

def chosen_plaintext_attack(encrypted_secret):
    secret = ''
    dataset = '0123456789abcddefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for enc in hex_array(encrypted_secret):
        for char in dataset:
            ciphertext = get_ciphertext(secret+char)
            cipher_byte = hex_array(ciphertext)[-1]
            print('trying character: "%s"' % char)
            if cipher_byte == enc:
                print('encrypted byte found: "%s"' % enc)
                secret += char
                break
    return secret

encrypted_secret = get_encrypted_secret()
secret = known_plaintext_attack(encrypted_secret)
if secret and len(secret) == len(encrypted_secret)/2:
    print('secret: "%s"' % secret)
else:
    print('secret not found!')
