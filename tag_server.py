#! /usr/bin/env python
# -*- coding :utf-8 -*-
from flask import *
import logging
import logging.handlers
import base64
import io
import datetime
from flask_apscheduler import APScheduler

#flask app
app = Flask(__name__)
#これを入れたらguncornから動かしてもいけた flask conf
app.config['DEBUG'] = True

scheduler = APScheduler()

#logの処理 下記はlogのbyte数を計測し、5000byteになったら別のlogファイルに出力され5つまでbackupする
#handler = logging.handlers.RotatingFileHandler("test.log", "a+", maxBytes=5000, backupCount=5)
handler = logging.handlers.TimedRotatingFileHandler(
    filename='log/tags.log',
    when='midnight'
)
#log出力部分の設定
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
app.logger.addHandler(handler)

#毎時何かしらの作業をする場合はこれで行う
@scheduler.task('cron',id='job01',hour='*')
def execute():
    pass

#entry.jsを返却するための関数
@app.route('/entry.js',methods=['GET', 'POST'])
def ajax_ddl():
    URL = 'http://localhost:5000/tag?'
    js = ""
    with open("tags.js","r",encoding="utf-8")as f:
        js_line = f.readlines()
        for i in js_line:
            js+=i.replace("¥n","")
    tmp = request.url.split("id=")
    js += 'var _imagePath = "'+URL+tmp[1]+'*" + now.getTime()+"*"+url+"*"+ref+"*"+cookie;'
    js += 'var _img = new Image(1,1);'
    js += '_img.src = _imagePath;'
    js += '_img.onload = function(){_void();}'
    resp = app.make_response(js)
    resp.mimetype = "text/JavaScript"
    return resp

#取得したlog情報を出力する関数
@app.route("/tag",methods=['GET', 'POST'])
def return_gif():
    URL = request.url.replace("%2F","/");
    app.logger.info(URL)
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='localhost', port=5000, threaded=True,debug=True)
