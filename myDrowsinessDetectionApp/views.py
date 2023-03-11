from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from flask import Flask, render_template, Response
from django.http import StreamingHttpResponse
from . import camera
from .models import Driver
from django.contrib import messages
from django.shortcuts import render
from django.core import serializers
from django.forms.models import model_to_dict

import json
from plotly.offline import plot
from plotly.graph_objs import Scatter
import cv2
import imutils
from imutils import face_utils
import dlib

def jsondata(result):
    data = list(result)
    return JsonResponse(data,safe = False)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def analytics(request):
    if 'user' not in request.session:
        return redirect('/')
    user = request.session.get('user')
    user = json.loads(user)
    context = {'user':user}
    return render(request, 'analytics.html',context)

# Dashboard
def index_show(request):
    if 'user' not in request.session:
        return redirect('/')
    user = request.session.get('user')
    user = json.loads(user)
    context = {'user':user}
    return render(request, 'index.html',context)


# Login
def pagelogin_show(request):
    
    if request.method == 'POST':
        email_address = request.POST.get('email_address')
        four_digit_pin = request.POST.get('four_digit_pin')
        if email_address=="" or four_digit_pin=="":
            messages.error(request,"Email Address and Four Digit PIN is requried")
            return redirect('/')
        try:
            driver = Driver.objects.get(email_address=email_address,four_digit_pin=four_digit_pin)
        except Driver.DoesNotExist:
            messages.error(request,"Please Enter valid Email address and Four Digit PIN")
            return redirect('/')
        #json_object = JsonResponse(list(driver),safe = False)
        #json_object=jsondata(driver)
        dict_obj = model_to_dict( driver )
        serialized = json.dumps(dict_obj)
        #print(serialized)
        #serialized_obj = serializers.serialize('json',  [driver] )
        #print(serialized_obj)
        #data = {"SomeModel_json": json_object}
        #print(data)
        request.session['user'] = serialized
        return redirect('index/')
    else:    
        return render(request, 'page_login.html')


# SignUp
def pageregister_show(request):
    if request.method == 'POST':
        email_address=request.POST.get('email_address')
        try:
            driver = Driver.objects.get(email_address=email_address)
        except Driver.DoesNotExist:
            save_record = Driver()
            save_record.first_name = request.POST.get('first_name')
            save_record.last_name = request.POST.get('last_name')
            save_record.email_address = request.POST.get('email_address')
            save_record.mobile_number = request.POST.get('mobile_number')
            save_record.four_digit_pin = request.POST.get('four_digit_pin')
            save_record.confirm_four_digit_pin = request.POST.get('confirm_four_digit_pin')
            save_record.daily_driving_hours = request.POST.get('daily_driving_hours')
            save_record.country = request.POST.get('country')
            save_record.gender = request.POST.get('gender')
            save_record.date_of_birth = request.POST.get('date_of_birth')
            save_record.vehicle_type = request.POST.get('vehicle_type')
            save_record.save()
            messages.success(request, 'Record saved successfully')
            return redirect('/')
        messages.success(request, 'User already exists')
        return render(request, 'page_register.html')
        
    else:
        return render(request, 'page_register.html')

def video_feed(request):
    return StreamingHttpResponse(gen(camera.VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')