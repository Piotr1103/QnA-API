from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage

import http.client, json
from qna.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

host = 'ehappyqna.azurewebsites.net'  #主機
endpoint_key = "b4017671-4d0e-4509-b9a3-3b12c4381495"  #授權碼
kb = "6630d109-8e7c-416e-82d8-fc32b5bbef5f"  #GUID碼
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

def sendUse(event):  #使用說明
    try:
        text1 ='''
這是台大醫院的疑難解答，
請輸入關於台大醫院相關問題。
               '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQnA(event, mtext):  #QnA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    if 'No good match' in result1:
        text1 = '很抱歉，資料庫中無適當解答！\n請再輸入問題。'
        #將沒有解答的問題寫入資料庫
        userid = event.source.user_id
        unit = users.objects.create(uid=userid, question=mtext)
        unit.save()
    else:
        result2 = result1[2:]  #移除「A：」
        text1 = result2  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token,message)
