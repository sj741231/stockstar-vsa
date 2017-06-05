#!/bin/bash


source ../env/bin/activate
export C_FORCE_ROOT="true"

base_dir=`pwd`
celery_pid() {
echo `ps auxf | grep -E "celery -A vsa worker" | grep -v grep| awk '{print $2}'`
}
start() {
 celery -A vsa worker -l debug --concurrency=10 --autoreload &>> $base_dir/celery.log 2>&1 &
 sleep 3
 pid=$(celery_pid)
 echo -e "\e[00;31mcelery is start (pid: $pid)\e[00m"
}



restart() {
 pid=$(celery_pid)
 echo -e "\e[00;31mcelery is restart (pid: $pid)\e[00m"
 ps auxf | grep -E "celery -A vsa worker" | grep -v grep| awk '{print $2}' | xargs kill -HUP &> /dev/null

}

stop() {
 pid=$(celery_pid)
 echo -e "\e[00;31mcelery is stop (pid: $pid)\e[00m"
 ps auxf | grep -E "celery -A vsa worker" | grep -v grep| awk '{print $2}' | xargs kill -TERM &> /dev/null

}
#restart(){
#    stop
#    start
#}

# See how we were called.
case "$1" in
  start)
        start
        ;;
  restart)
        restart
        ;;

  stop)
        stop
        ;;

  *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 2
esac







#nohup celery -A vsa worker -l debug --concurrency=10 --autoreload  & >>celery.log