# from django.shortcuts import render, redirect
# from decouple import config
# from pprint import pprint
# import requests

# from .forms import CityForm
# from .models import City
# from django.contrib import messages

# # Create your views here.

# def index(request):
#     form = CityForm()
#     cities = City.objects.all()
#     url = config('BASE_URL')
#     city = 'Berlin'
#     # r = requests.get(url.format(city))
#     # content = r.json()
#     # print(type(content ))
#     # pprint(content )
#     # print('jjxx')
    
#     if request.method == 'POST':
#         form = CityForm(request.POST) # request.post.get('name')
#         if form.is_valid():
#             new_city = form.cleaned_data['name']
#             if not City.objects.filter(name=new_city).exists():
#                 form.save()
#             else:
#                 messages.warning(request, 'City already exist')
                
                
#             form.save()
#             return redirect('home')
#     city_data = []
#     for city in cities:
#         print(city)
#         r = requests.get(url.format(city))
#         content = r.json()
        
#         weather_data = {
#         'city': city.name,
#         'temp': content['main']['temp'],
#         'description':content['weather'][0]['description'],
#         'icon':content['weather'][0]['icon'],
#     }
#         city_data.append(weather_data)
#     context = {
#             'city_data': city_data,
#             'form': form
#         }
#     return render(request, "weatherapp/index.html", context)
from django.shortcuts import redirect, render
from decouple import config
import requests
from pprint import pprint

from .forms import CityForm
from .models import City
from django.contrib import messages


def index(request):
    # 'api.openweathermap.org/data/2.5/weather?q={}&appid=&units=metric'.format("Berlin")
    form = CityForm()
    cities = City.objects.all()
    url = config("BASE_URL")

    # content = r.json()
    # print(type(a))
    # pprint(a)

    if request.method == "POST":
        form = CityForm(request.POST)  # request.POST.get("name")
        if form.is_valid():
            new_city = form.cleaned_data["name"]
            if not City.objects.filter(name=new_city).exists():
                r = requests.get(url.format(new_city))
                if r.status_code == 200:
                    form.save()
                    messages.success(request, "City added succesfully!")
                else:
                    messages.warning(request, "City does not exist.")
            else:
                messages.warning(request, "City already exists.")
            return redirect("home")

    city_data = []
    for city in cities:
        print(city)
        r = requests.get(url.format(city))
        # print(r.status_code)
        content = r.json()

        weather_data = {
            "city": city.name,
            "temp": content["main"]["temp"],
            "description": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"]
        }

        city_data.append(weather_data)
    print(city_data)

    context = {
        "city_data": city_data,
        "form": form
    }
    return render(request, "weatherapp/index.html", context)
