#!/usr/bin/env bash

source ../env/bin/activate

base_dir=`pwd`
vsystem_pid() {
echo `ps auxf | grep -E "(manage.py)(.*):8080" | grep -v grep| awk '{print $2}'`
}
start() {
 python $base_dir/manage.py runserver 0.0.0.0:8080 &>> $base_dir/django.log 2>&1 &
 pid=$(vsystem_pid)
 echo -e "\e[00;31mVsystem is running (pid: $pid)\e[00m"
}

stop() {
 pid=$(vsystem_pid)
 echo -e "\e[00;31mVsystem is stop (pid: $pid)\e[00m"
 ps auxf | grep -E "(manage.py)(.*):8080" | grep -v grep| awk '{print $2}' | xargs kill -9 &> /dev/null

}

restart(){
    stop
    start
}

# See how we were called.
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;

  restart)
        restart
        ;;

  *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 2
esac