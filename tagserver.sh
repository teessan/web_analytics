#!/bin/sh
PROGNAME=`basename $0`
BASEDIR=`dirname $0`
PIDFILE=$BASEDIR/$PROGNAME.pid
#echo ${PROGNAME}
#echo ${BASEDIR}
#echo ${PIDFILE}

start() {
    echo "Starting server..."
    cd ${BASEDIR}
    #-Dでデーモン化、-wでワーカーの数を指定 -p でPID保存用のファイルを出力
    #configファイルを指定
    gunicorn tag_server:app -p ${PIDFILE} -D -b localhost:5000 -w 2 --log-file /tmp/tags.log --log-level debug
}

stop(){
    echo "Stopping server..."
    kill -TERM `cat ${PIDFILE}`
    rm -f ${PIDFILE}
}

usage(){
    echo "usage: ${PROGNAME} start|stop|restart"
}

if [ $# -lt 1 ]; then
    usage
    exit 255
fi

case $1 in
    start) start ;;
    stop)  stop  ;;
    restart) stop start ;;
    *) usage;;
esac
