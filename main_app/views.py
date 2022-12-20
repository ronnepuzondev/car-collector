from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Car, Accessory
from .forms import MaintenanceForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Add the following import
from django.http import HttpResponse

# Define the home view
def home(request):
    return render(request, "home.html")

    # Create your views here.


def about(request):
    return render(request, "about.html")

@login_required
def cars_index(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, "cars/index.html", {"cars": cars})

@login_required
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

@login_required
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

@login_required
def assoc_accessory(request, car_id, accessory_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Car.objects.get(id=car_id).accessories.add(accessory_id)
    return redirect("detail", car_id=car_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class CarCreate(CreateView):
    model = Car
    fields = ['name', 'model', 'description', 'age']
    success_url = "/cars/"
    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


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
