from django.http.response import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render
import pandas as pd
import numpy as np
# Create your views here.
from django.http import HttpResponse
import json

def index(request):
    idiom = request.GET.get("idiom")
    chengyu = pd.read_json("./wx_chengyu_api/data/idiom.json")
    chengyu = chengyu.set_index("word") 
    chengyu_jielong = {}
    num = 0
    if idiom not in chengyu.index:
        return HttpResponse("这不是一个成语",status=501)
    else:
        words = chengyu.index[chengyu["shoupin"] == chengyu.loc[idiom,"weipin"]]
        #return HttpResponse("随机显示成语：")
        word1 = np.random.choice(words)
        chengyu_jielong[num] = word1
    while True:
        words = chengyu.index[chengyu["shoupin"] == chengyu.loc[word1,"weipin"]]
        if words.shape[0] == 0:
            break
        word1 = np.random.choice(words)
        num = num+1
        chengyu_jielong[num] = word1
    print(chengyu_jielong)
    return HttpResponse(json.dumps(chengyu_jielong,ensure_ascii=False),content_type="application/json,charset=utf-8")
#初始化
def init(request):
    chengyu = pd.read_json("./wx_chengyu_api/data/idiom.json")
    chengyu = chengyu.set_index("word")
    #提供挑战开始的成语
    startidoim = np.random.choice(chengyu.index)
    return HttpResponse(startidoim)

#开始对战
def battle(request):    
    aiidiom = request.GET.get("aiidiom")
    useridiom = request.GET.get("useridiom")
    chengyu = pd.read_json("./wx_chengyu_api/data/idiom.json")
    chengyu = chengyu.set_index("word")
    weipin = chengyu.loc[aiidiom,"weipin"]
    if useridiom not in chengyu.index:
        return HttpResponse("这不是一个成语",status=501)
    if chengyu.loc[useridiom,"shoupin"] != weipin:
        return HttpResponse("输入的成语不能与机器人出的成语接上",status=502)
    aiidioms = chengyu.index[chengyu["shoupin"] == chengyu.loc[useridiom,"weipin"]]
    if aiidioms.shape[0] == 0:
        return HttpResponse("恭喜你打败了机器人",status=666)
    aiidiom = np.random.choice(aiidioms)
    return HttpResponse(aiidiom)