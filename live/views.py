from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import video,LiveNode

# Create your views here.

@login_required()
def monitor_video(request,pk):
    live = get_object_or_404(video,pk=pk)
    return render(request,'video_monitor.html',locals())

@login_required()
def watch_video(request, pk):
    video = get_object_or_404(LiveNode,pk=pk)
    return  render(request,'watch.html',locals())


@login_required()
def mobile_play(request,pk):
    video = get_object_or_404(LiveNode,pk=pk)
    return render(request,'mobile_play.html',locals())


@login_required()
def player(request):
    return render(request,'player.html')