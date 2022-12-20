from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Car, Accessory
from .forms import MaintenanceForm

# Add the following import
from django.http import HttpResponse

# Define the home view
def home(request):
    return render(request, "home.html")

    # Create your views here.


def about(request):
    return render(request, "about.html")


def cars_index(request):
    cars = Car.objects.all()
    return render(request, "cars/index.html", {"cars": cars})


def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    id_list = car.accessories.all().values_list("id")
    accessories_car_doesnt_have = Accessory.objects.exclude(id__in=id_list)
    maintenance_form = MaintenanceForm()
    return render(
        request,
        "cars/detail.html",
        {
            "car": car,
            "maintenance_form": maintenance_form,
            "accessories": accessories_car_doesnt_have,
        },
    )


def add_maintenance(request, car_id):
    # create a ModelForm instance using the data in request.POST
    form = MaintenanceForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_maintenance = form.save(commit=False)
        new_maintenance.car_id = car_id
        new_maintenance.save()
    return redirect("detail", car_id=car_id)


def assoc_accessory(request, car_id, accessory_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Car.objects.get(id=car_id).accessories.add(accessory_id)
    return redirect("detail", car_id=car_id)


class CarCreate(CreateView):
    model = Car
    fields = "__all__"
    success_url = "/cars/"


class CarUpdate(UpdateView):
    model = Car
    # Let's disallow the renaming of a car by excluding the name field!
    fields = ["model", "description", "age"]


class CarDelete(DeleteView):
    model = Car
    success_url = "/cars/"


class AccessoryList(ListView):
    model = Accessory


class AccessoryDetail(DetailView):
    model = Accessory


class AccessoryCreate(CreateView):
    model = Accessory
    fields = "__all__"


class AccessoryUpdate(UpdateView):
    model = Accessory
    fields = "__all__"


class AccessoryDelete(DeleteView):
    model = Accessory
    success_url = "/Accessories/"
