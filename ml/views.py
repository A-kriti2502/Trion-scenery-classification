from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import auth, User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage

from .apps import MlConfig
from .decorators import unauthenticated_user

import json
import numpy as np

from keras.models import load_model
import tensorflow as tf
from keras.preprocessing import image
from tensorflow.python.keras.backend import set_session



# Create your views here.

img_height, img_width=180,180

import os


@login_required(login_url='login')
def predictImage3(request):
    with open('./models/reverse_Climateclass_dictionary.json','r') as f:
        climate_labelInfo=f.read()

    climate_labelInfo=json.loads(climate_labelInfo)

    if request.method == 'POST':
        file = request.FILES['filepath']
        file_name = default_storage.save(file.name, file)
        filepathName = default_storage.path(file_name)
        testimage=filepathName
        img = image.load_img(testimage, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x=x/255.0
        x=x.reshape(-1,img_height, img_width,3)
        pred= settings.CLIMATE_MODEL.predict(x)


        # no = np.argmax(pred[0])
        predictedLabel=climate_labelInfo[str(np.argmax(pred[0]))]
        print(predictedLabel)
        txt = "Empty image"
        if predictedLabel == 'Cloudy':
            txt = "Cloudy comes from the Old English word clud, 'mass of rock,' and later 'cloud,' based on the way a cloud can resemble a rock or hill.\nWhen the sky is cloudy, it's so full of clouds that you can't see the sun. A cloudy day isn't ideal for a trip to the beach, and a cloudy night isn't great for star gazing."
        elif predictedLabel == 'Rain':
            txt = "When the sky is cloudy, it's so full of clouds that you can't see the sun. A cloudy day isn't ideal for a trip to the beach, and a cloudy night isn't great for star gazing."
        elif predictedLabel == 'Shine':
            txt = "On Earth, sunlight is scattered and filtered through Earth's atmosphere, and is obvious as daylight when the Sun is above the horizon. When direct solar radiation is not blocked by clouds, it is experienced as sunshine, a combination of bright light and radiant heat."
        elif predictedLabel == 'SunRise':
            txt = "Sunrise (or sunup) is the moment when the upper rim of the Sun appears on the horizon in the morning. The term can also refer to the entire process of the solar disk crossing the horizon and its accompanying atmospheric effects."
        else:
            txt = 'Can Not Classify the image or an error occured'

        para ={'filepathName':'../media/'+file_name,'predictedLabel':predictedLabel, "x":img,'text':txt}
        return render(request, 'ml/displayimg2.html',para)

    else:
        para ={}
        return render(request, 'ml/imgUpload2.html',para)



@login_required(login_url='login')
def predictImage2(request):
    with open('./models/reverse_Terrainclass_dictionary.json','r') as f:
        terrain_labelInfo=f.read()


    terrain_labelInfo=json.loads(terrain_labelInfo)

    if request.method == 'POST':
        file = request.FILES['filepath']
        file_name = default_storage.save(file.name, file)
        filepathName = default_storage.path(file_name)
        testimage=filepathName
        img = image.load_img(testimage, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x=x/255.0
        x=x.reshape(-1,img_height, img_width,3)
        pred= settings.TERRAIN_MODEL.predict(x)
        no = np.argmax(pred[0])
        predictedLabel=terrain_labelInfo[str(no)]
        print(predictedLabel)
        txt = ""
        if predictedLabel == 'buildings':
            txt = '''A building, or edifice, is a structure with a roof and walls standing more or less permanently in one place, such as a house or factory.Buildings come in a variety of sizes, shapes, and functions, and have been adapted throughout history for a wide number of factors, from building materials available, to weather conditions, land prices, ground conditions, specific uses, and aesthetic reasons. To better understand the term building compare the listof nonbuilding structures.'''
            
        elif predictedLabel == 'forest':
            txt = "A forest is a piece of land with many trees. Forests are very important and grow in many places around the world. They are an ecosystem which includes many plants and animals. Temperature and rainfall are the two most important things for forests. Forests can exist from the equator to near the polar regions, but different climates have different kinds of forests. In cold climates conifers dominate, but in temperate zone and tropical climates forests are mainly made up of flowering plants."

        elif predictedLabel == 'glacier':
            txt = "A glacier is a persistent body of dense ice that is constantly moving under its own weight. A glacier forms where the accumulation of snow exceeds its ablation over many years, often centuries. Glaciers slowly deform and flow under stresses induced by their weight, creating crevasses, seracs, and other distinguishing features. They also abrade rock and debris from their substrate to create landforms such as cirques, moraines, or fjords. Glaciers form only on land and are distinct from the much thinner sea ice and lake ice that forms on the surface of bodies of water."

        elif predictedLabel == 'mountain':
            txt = "A mountain is an elevated portion of the Earth's crust, generally with steep sides that show significant exposed bedrock. A mountain differs from a plateau in having a limited summit area, and is larger than a hill, typically rising at least 300 metres (1000 feet) above the surrounding land.Mountains are formed through tectonic forces, erosion, or volcanism,[1] which act on time scales of up to tens of millions of years."

        elif predictedLabel == 'sea':
            txt = "The sea, connected as the world ocean or simply the ocean, is the body of salty water that covers over 70 percent of the Earth's surface. The word sea is also used to denote second-order sections of the sea, such as the Mediterranean Sea, as well as certain large, entirely landlocked, saltwater lakes, such as the Caspian Sea.The sea moderates Earth's climate and has important roles in the water cycle, carbon cycle, and nitrogen cycle."

        elif predictedLabel == 'street':
            txt = "A street is a public thoroughfare in a built environment. It is a public parcel of land adjoining buildings in an urban context, on which people may freely assemble, interact, and move about. A street can be as simple as a level patch of dirt, but is more often paved with a hard, durable surface such as tarmac, concrete, cobblestone or brick. Portions may also be smoothed with asphalt, embedded with rails, or otherwise prepared to accommodate non-pedestrian traffic."
        else:
            txt = 'Can Not Classify the image or an error occured'
     


        para ={'filepathName':'../media/'+file_name,'predictedLabel':predictedLabel,"x":img,'text':txt}
        return render(request, 'ml/displayimg.html',para)

    else:
        para ={}
        return render(request, 'ml/imgUpload_copy.html',para)



def home(request):
    return render(request,'ml/home.html')


@login_required(login_url='login')
def displayimg(request):
    return render(request,'ml/displayimg.html')


@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if username is not None:
            if password is not None:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Already Taken')
                    return redirect('signup')

                else:
                    user = User.objects.create_user(username=username,email=email, password=password)
                    user.save()
                    return render(request, 'ml/index2.html')
            else:
                messages.info(request, 'Password Input Empty')
                return redirect('signup')
        else:
            messages.info(request, 'Username Input Empty')
            return redirect('signup')
    else:
        return render(request, "ml/signup.html")


@unauthenticated_user
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Sorry, your username or password was incorrect.')
            return redirect('login')
    
    else:
        return render(request, 'ml/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login')
def imgUpload(request):
    para = {}
    return render(request, 'ml/imgUpload.html',para)