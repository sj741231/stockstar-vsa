#!/bin/bash
source ../../env/bin/activate
 
r=`stty size| awk {'print $1'}`
c=`stty size| awk {'print $2'}`
#if [ $USER == 'admin' ] || [ $USER == 'root' ];then
#  echo ""
#else
  python login.py $r $c
#fi
