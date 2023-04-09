# ================
# 注：
# (这其实是我第一次用python这门语言QAQ）
# 代码有冗长/不好之处还请多多见谅
# ===============

import requests
import json
import time
import pyautogui
import os
import urllib
import urllib3
import random
import hashlib
import http
import uuid
import sys
from imp import reload
from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models
count = 0

urllib3.disable_warnings()

reload(sys)

# 有道翻译API
YOUDAO_URL = 'https://openapi.youdao.com/api'
# 你的 有道翻译API 密钥等
APP_KEY = 'xxxx'
APP_SECRET = 'xxxxx'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers, verify=False)


def YouDaoTranslate(word):
    data = {}
    data['from'] = 'en'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = word
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    time.sleep(1)
    return (response.json()['web'])


# 阿里云翻译API
ACCESS_KEY_ID = 'xxxxx'
ACCESS_KEY_SECRET = 'xxxxxx'


def create_client(
    access_key_id: str,
    access_key_secret: str,
) -> alimt20181012Client:
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    config.endpoint = f'mt.cn-hangzhou.aliyuncs.com'
    return alimt20181012Client(config)


def ALiYuntranslate(word, flag=1):
    client = create_client(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    if flag:
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            format_type='text',
            source_language='en',
            target_language='zh',
            source_text=word,
            scene='general'
        )
    else:
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            format_type='text',
            source_language='zh',
            target_language='en',
            source_text=word,
            scene='general'
        )
    runtime = util_models.RuntimeOptions()
    resp = client.translate_general_with_options(translate_general_request, runtime)
    return resp.body.data.__dict__['translated']


# 百度翻译API
def baiduTranslate(translate_text, flag=1):
    appid = 'xxxxxxx'  # appid
    secretKey = 'xxxxxxxxxxxx'  # 密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址
    fromLang = 'auto'  # 原文语种

    if flag:
        toLang = 'en'  # 译文语种
    else:
        toLang = 'zh'  # 译文语种

    salt = random.randint(3276, 65536)

    sign = appid + translate_text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(translate_text) + '&from=' + fromLang + \
        '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # return result
        return result['trans_result'][0]['dst']

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False


def AutoFillAnswer():
    # A (1450, 392)
    # B (1450, 470)
    # C (1450, 552)
    # D (1450, 640)
    # SKIP (2000, 1250)
    # 此处需要自测屏幕位置【详见GetAnswerPlace.py】
    pyautogui.FAILSAFE = True

    number = 1

    print('---5s后将开始答题---请不要操作鼠标---')
    time.sleep(5)

    with open('answer.txt', 'r', encoding='utf-8') as A:
        for i in A:
            answer = i.strip()
            if answer == 'A':
                pyautogui.moveTo(1450, 392, duration=0.1)
                time.sleep(0.3)
                pyautogui.click()
            if answer == 'B':
                pyautogui.moveTo(1450, 470, duration=0.1)
                time.sleep(0.3)
                pyautogui.click()
            if answer == 'C':
                pyautogui.moveTo(1450, 552, duration=0.1)
                time.sleep(0.3)
                pyautogui.click()
            if answer == 'D':
                pyautogui.moveTo(1450, 640, duration=0.1)
                time.sleep(0.3)
                pyautogui.click()
            if answer == 'Not Found':
                pyautogui.moveTo(2000, 1250, duration=0.1)
                time.sleep(0.3)
                pyautogui.click()
            print(f'[+] 答题中... | 本题答案：{i}  |  当前进度{number}/100')
            number += 1

    print('===答题结束===')


def PrintAnswer():
    number = 1
    print('===按下回车键以依次查看答案！===')
    with open('answer.txt', 'r', encoding='utf-8') as A:
        for i in A:
            if (input() == ''):
                print('{} '.format(number))
                print(i.strip())
                number += 1
    print('Over!')


def translate(word):
    url = 'https://fanyi.baidu.com/sug'
    data = {'kw': word}
    return str(json.loads(requests.post(url, data=data, verify=False).text))


def CheckFormat(old_str, new_str):
    file_data = ""
    with open('questions.json', 'r', encoding='utf-8') as old_file:
        for i in old_file:
            if old_str in i:
                i = i.replace(old_str, new_str)
            file_data += i
    with open('questions.json', 'w', encoding='utf-8') as new_file:
        new_file.write(file_data)


def CheckAnswer(answer):
    if answer == i['word']:
        return 0


def SaveAnswer(answer):
    with open('answer.txt', 'a', encoding='utf-8') as A:
        A.write(answer + '\n')
    return 1


# 测试正确率 / 测试用
def TestRight(answer):
    if answer == i['answer']:
        print('YES')
        return 1
    else:
        print('NO')
        return 0


# def OpenCET4():
#     with open('I love Words/cet-4.json', 'r', encoding='utf-8') as cet4_json:
#         cet4_data = json.load(cet4_json)
#     return cet4_data


# 保证问题格式
CheckFormat('（', '(')
CheckFormat('）', ')')
CheckFormat('……', '...')
CheckFormat('…', '...')
CheckFormat(' . ', '')
CheckFormat('  . ', '')
CheckFormat('. ', '')
CheckFormat('.', '')
CheckFormat('，', ',')
CheckFormat('、', ',')


# 读取json
with open('I love Words/cet-4 copy.json', 'r', encoding='utf-8') as cet4_json:
    cet4_data = json.load(cet4_json)
with open('I love Words/cet-6.json', 'r', encoding='utf-8') as cet6_json:
    cet6_data = json.load(cet6_json)
with open('I love Words/New.json', 'r', encoding='utf-8') as main:
    main_data = json.load(main)
with open('I love Words/questions.json', 'r', encoding='utf-8') as Q:
    Q_data = json.load(Q)
# print(Q_data)

QuestionNumber = 0
result = 0

# 查答案
for i in Q_data['list']:
    QuestionNumber += 1
    word = i['title']
    print('[+]', QuestionNumber, word)
    for x in main_data:
        if x['Q'] == word:
            if i['answerA'] == x['A']:
                answer = 'A'
                result = 1
            elif i['answerB'] == x['A']:
                answer = 'B'
                result = 1
            elif i['answerC'] == x['A']:
                answer = 'C'
                result = 1
            elif i['answerD'] == x['A']:
                answer = 'D'
                result = 1
    if i['cet'] == 4:
        if not is_Chinese(word):
            for j in cet4_data:
                if j['Word'] == word:
                    if i['answerA'] in j['Mean']:
                        answer = 'A'
                        result = 1
                    elif i['answerB'] in j['Mean']:
                        answer = 'B'
                        result = 1
                    elif i['answerC'] in j['Mean']:
                        answer = 'C'
                        result = 1
                    elif i['answerD'] in j['Mean']:
                        answer = 'D'
                        result = 1
        else:
            for k in cet4_data:
                if word in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
    if i['cet'] == 6:
        if not is_Chinese(word):
            for j in cet6_data:
                if j['Word'] == word:
                    if i['answerA'] in j['Mean']:
                        answer = 'A'
                        result = 1
                    elif i['answerB'] in j['Mean']:
                        answer = 'B'
                        result = 1
                    elif i['answerC'] in j['Mean']:
                        answer = 'C'
                        result = 1
                    elif i['answerD'] in j['Mean']:
                        answer = 'D'
                        result = 1
        else:
            for k in cet6_data:
                if word in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
    if result != 1:
        if i['cet'] == 6:
            if not is_Chinese(word):
                for j in cet4_data:
                    if j['Word'] == word:
                        if i['answerA'] in j['Mean']:
                            answer = 'A'
                            result = 1
                        elif i['answerB'] in j['Mean']:
                            answer = 'B'
                            result = 1
                        elif i['answerC'] in j['Mean']:
                            answer = 'C'
                            result = 1
                        elif i['answerD'] in j['Mean']:
                            answer = 'D'
                            result = 1
            else:
                for k in cet4_data:
                    if word in k['Mean']:
                        if i['answerA'] == k['Word']:
                            answer = 'A'
                            result = 1
                        if i['answerB'] == k['Word']:
                            answer = 'B'
                            result = 1
                        if i['answerC'] == k['Word']:
                            answer = 'C'
                            result = 1
                        if i['answerD'] == k['Word']:
                            answer = 'D'
                            result = 1
        if i['cet'] == 4:
            if not is_Chinese(word):
                for j in cet6_data:
                    if j['Word'] == word:
                        if i['answerA'] in j['Mean']:
                            answer = 'A'
                            result = 1
                        elif i['answerB'] in j['Mean']:
                            answer = 'B'
                            result = 1
                        elif i['answerC'] in j['Mean']:
                            answer = 'C'
                            result = 1
                        elif i['answerD'] in j['Mean']:
                            answer = 'D'
                            result = 1
            else:
                for k in cet6_data:
                    if word in k['Mean']:
                        if i['answerA'] == k['Word']:
                            answer = 'A'
                            result = 1
                        if i['answerB'] == k['Word']:
                            answer = 'B'
                            result = 1
                        if i['answerC'] == k['Word']:
                            answer = 'C'
                            result = 1
                        if i['answerD'] == k['Word']:
                            answer = 'D'
                            result = 1
    if result != 1:
        if not is_Chinese(word):
            transResult = translate(word)
            if i['answerA'] in transResult:
                answer = 'A'
                result = 1
            if i['answerB'] in transResult:
                answer = 'B'
                result = 1
            if i['answerC'] in transResult:
                answer = 'C'
                result = 1
            if i['answerD'] in transResult:
                answer = 'D'
                result = 1
            time.sleep(0.3)
        else:
            transResult = translate(i['answerA'])
            if word in transResult:
                answer = 'A'
                result = 1
            transResult = translate(i['answerB'])
            if word in transResult:
                answer = 'B'
                result = 1
                time.sleep(0.3)
            transResult = translate(i['answerC'])
            if word in transResult:
                answer = 'C'
                result = 1
            transResult = translate(i['answerD'])
            if word in transResult:
                answer = 'D'
                result = 1
            time.sleep(0.3)
    if result != 1 and ',' in word:
        word_clip1 = word.split(',')[0]
        word_clip2 = word.split(',')[1]
        if i['cet'] == 4:
            for k in cet4_data:
                if word_clip1 in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
        if i['cet'] == 6:
            for k in cet6_data:
                if word_clip1 in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
        if i['cet'] == 4:
            for k in cet4_data:
                if word_clip2 in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
        if i['cet'] == 6:
            for k in cet6_data:
                if word_clip2 in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
    if result != 1:
        if not is_Chinese(word):
            transResult = baiduTranslate(word, flag=1)
            if i['answerA'] in transResult or transResult in i['answerA']:
                answer = 'A'
                result = 1
            if i['answerB'] in transResult or transResult in i['answerB']:
                answer = 'B'
                result = 1
            if i['answerC'] in transResult or transResult in i['answerC']:
                answer = 'C'
                result = 1
            if i['answerD'] in transResult or transResult in i['answerD']:
                answer = 'D'
                result = 1
            time.sleep(0.3)
        else:
            transResult = baiduTranslate(word, flag=0)
            if i['answerA'] in transResult or transResult in i['answerA']:
                answer = 'A'
                result = 1
            if i['answerB'] in transResult or transResult in i['answerB']:
                answer = 'B'
                result = 1
            if i['answerC'] in transResult or transResult in i['answerC']:
                answer = 'C'
                result = 1
            if i['answerD'] in transResult or transResult in i['answerD']:
                answer = 'D'
                result = 1
            time.sleep(0.3)
    if result != 1:
        if is_Chinese(word):
            transResult = baiduTranslate(i['answerA'], flag=1)
            if word in transResult or transResult in word:
                answer = 'A'
                result = 1
            transResult = baiduTranslate(i['answerB'], flag=1)
            if word in transResult or transResult in word:
                answer = 'B'
                result = 1
                time.sleep(0.3)
            transResult = baiduTranslate(i['answerC'], flag=1)
            if word in transResult or transResult in word:
                answer = 'C'
                result = 1
            transResult = baiduTranslate(i['answerD'], flag=1)
            if word in transResult or transResult in word:
                answer = 'D'
                result = 1
            time.sleep(0.3)
        else:
            transResult = baiduTranslate(i['answerA'], flag=0)
            if word in transResult or transResult in word:
                answer = 'A'
                result = 1
            transResult = baiduTranslate(i['answerB'], flag=0)
            if word in transResult or transResult in word:
                answer = 'B'
                result = 1
                time.sleep(0.3)
            transResult = baiduTranslate(i['answerC'], flag=0)
            if word in transResult or transResult in word:
                answer = 'C'
                result = 1
            transResult = baiduTranslate(i['answerD'], flag=0)
            if word in transResult or transResult in word:
                answer = 'D'
                result = 1
            time.sleep(0.3)
    if result != 1:
        if not is_Chinese(word):
            transResult = ALiYuntranslate(word, flag=1)
            if i['answerA'] in transResult or transResult in i['answerA']:
                answer = 'A'
                result = 1
            if i['answerB'] in transResult or transResult in i['answerB']:
                answer = 'B'
                result = 1
            if i['answerC'] in transResult or transResult in i['answerC']:
                answer = 'C'
                result = 1
            if i['answerD'] in transResult or transResult in i['answerD']:
                answer = 'D'
                result = 1
        else:
            transResult = ALiYuntranslate(word, flag=0)
            if i['answerA'] in transResult or transResult in i['answerA']:
                answer = 'A'
                result = 1
            if i['answerB'] in transResult or transResult in i['answerB']:
                answer = 'B'
                result = 1
            if i['answerC'] in transResult or transResult in i['answerC']:
                answer = 'C'
                result = 1
            if i['answerD'] in transResult or transResult in i['answerD']:
                answer = 'D'
                result = 1
    if result != 1:
        if is_Chinese(word):
            transResult = ALiYuntranslate(i['answerA'], flag=1)
            if word in transResult or transResult in word:
                answer = 'A'
                result = 1
            transResult = ALiYuntranslate(i['answerB'], flag=1)
            if word in transResult or transResult in word:
                answer = 'B'
                result = 1
            transResult = ALiYuntranslate(i['answerC'], flag=1)
            if word in transResult or transResult in word:
                answer = 'C'
                result = 1
            transResult = ALiYuntranslate(i['answerD'], flag=1)
            if word in transResult or transResult in word:
                answer = 'D'
                result = 1
        else:
            transResult = ALiYuntranslate(i['answerA'], flag=0)
            if word in transResult or transResult in word:
                answer = 'A'
                result = 1
            transResult = ALiYuntranslate(i['answerB'], flag=0)
            if word in transResult or transResult in word:
                answer = 'B'
                result = 1
            transResult = ALiYuntranslate(i['answerC'], flag=0)
            if word in transResult or transResult in word:
                answer = 'C'
                result = 1
            transResult = ALiYuntranslate(i['answerD'], flag=0)
            if word in transResult or transResult in word:
                answer = 'D'
                result = 1
    if result != 1 and not is_Chinese(word):
        if i['cet'] == 4:
            for k in cet4_data:
                if word in k['Mean']:
                    countNum = 0
                    Alist = list(i['answerA'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'A'
                        result = 1
                    countNum = 0
                    Alist = list(i['answerB'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'B'
                        result = 1
                    countNum = 0
                    Alist = list(i['answerC'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'C'
                        result = 1
                    countNum = 0
                    Alist = list(i['answerD'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'D'
                        result = 1
        if i['cet'] == 6:
            for k in cet6_data:
                if word in k['Mean']:
                    countNum = 0
                    Alist = list(i['answerA'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'A'
                        result = 1
                    countNum = 0
                    Alist = list(i['answerB'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'B'
                        result = 1
                    countNum = 0
                    Alist = list(i['answerC'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'C'
                        result = 1
                    countNum = 0
                    Alist = list(i['answerD'])
                    for x in Alist:
                        if x in k['Word']:
                            countNum += 1
                    if countNum/len(Alist) >= 0.5:
                        answer = 'D'
                        result = 1
    if result != 1:
        if i['cet'] == 6:
            for k in cet4_data:
                if word in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
        if i['cet'] == 4:
            for k in cet6_data:
                if word in k['Mean']:
                    if i['answerA'] == k['Word']:
                        answer = 'A'
                        result = 1
                    if i['answerB'] == k['Word']:
                        answer = 'B'
                        result = 1
                    if i['answerC'] == k['Word']:
                        answer = 'C'
                        result = 1
                    if i['answerD'] == k['Word']:
                        answer = 'D'
                        result = 1
    if result != 1:
        answer = 'Not Found'
        print('[x] Not Found!')
        print('[!]', word)
        SaveAnswer(answer)
    else:
        result = 0
        SaveAnswer(answer)
        print('[√] Found!')
        count += TestRight(answer)

print('[*] 查找答案已完成！')
print('\n')
print('===请将模拟器最大化于屏幕二，并保证界面无遮挡===')
print('\n')

# 自动答题 / 模拟器用户
AutoFillAnswer()

# 看具体每道题 /非模拟器用户
# PrintAnswer()

os.remove('I love Words/answer.txt')

# questions.json 中有答案情况(*test)
# print('正确率：', count, '%')
