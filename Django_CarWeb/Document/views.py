from django.http import *
import numpy as np
from open3d import read_point_cloud
from plotly.offline import plot
import plotly.graph_objs as go
from django.shortcuts import redirect, render ,get_object_or_404,render_to_response
from django.views.generic import View , ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from . forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.contrib import messages
from django.contrib.postgres.fields import JSONField

from django.contrib.auth import update_session_auth_hash



# **************************************************************************** LOGIN / REGISTRO ***************************************************************#

def logout_view(request):#Función para desloguearte
    logout(request)
    return redirect('../../')


class LoginFormView(View): #Vista que se encarga del login del usuario.
    form_class = LoginForm
    template_name = 'Document/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('../list')
            else:
                messages.error(request, 'La contraseña o usuario es erróneo!')

        return render(request, self.template_name, {'form': form})




class RegisterFormView(View): # vista que se encarga del nuevo registro de un usuario
    form_class = RegisterForm
    template_name = 'Document/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('../')

        return render(request, self.template_name, {'form': form})


#********************************************************************** LISTAS ************************************************************************************#


class list(ListView):

    model = Document
    template_name = 'Document/list.html'
    paginate_by = 7
    context_object_name = "object_list"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(numb__icontains=query).filter(user=self.request.user).order_by('numb')
            return object_list
        else:
            return Document.objects.filter(user=self.request.user).order_by('numb')



#******************************************************************************** SUBIR ARCHIVOS *************************************************************************************#

def simple_upload(request): # Con esta función definimos cómo subir varios Documentos

        user = request.user
        if request.method == "POST":
            files = request.FILES.getlist('myfiles')

            for number, file in enumerate(files):
                value = str(file) #Pasamos el nombre de cada fichero que queremos subir a la variable "value"
                value = re.sub("\D", "", value) #Remueve todo del string excepto los digitos
                instance = Document( #Guardamos el nombre del documento, el numero del usuario y el de cada fichero que hemos subido en la base de datos
                           document = file,
                           Nombre = file,
                           user = user,
                           numb = value)

                if Document.objects.filter(Nombre = instance.Nombre).filter(user=request.user).exists():

                    messages.error(request, 'La contraseña o usuario es erróneo!')
                    pass

                else:
                    instance.save()
            request.session['number_of_files'] = number + 1
            return redirect('../list')

#*****************************************************************************************  BORRAR ARCHIVOS ******************************************************************************************#



def delete_view(request, id): # borramos el documento que hayamos escogido anteriormente

        obj = get_object_or_404(Document, id=id)
        if request.method == "POST":
            obj.delete()
            return redirect('list')
        context = {
            "object": obj
        }




#****************************************************************************************** CREAR PCL ***********************************************************#


def create_image(request, numb, ):  # Representación Nube de puntos.

    from decimal import Decimal
    import json
    document = Document.objects.filter(user=request.user).get(numb=numb)
    filename = document.document.path

    gps_north = document.gps_northing
    gps_easting = document.gps_easting
    gps_lat = document.gps_lat
    gps_long = document.gps_long
    layers = document.layers

    str_gps_long = []
    str_gps_lat = []

    if gps_long != None:

        for i in gps_long:
            str_gps_long.append(json.dumps(str(Decimal(i))))

        str_gps_long = ", ".join([i.replace('"', '') for i in str_gps_long])


    if gps_lat != None:

        for i in gps_lat:
            str_gps_lat.append(json.dumps(str(Decimal(i))))


        str_gps_lat =", ".join( [i.replace('"', '') for i in str_gps_lat])


    nombre = document.Nombre



    pcd = read_point_cloud(filename)
    pcd_array = (np.asarray(pcd.points))

    x = []
    y = []
    z = []


    for row in pcd_array:
        x.append(float(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))




    form = clasificadorform(request.POST or None)
    if request.is_ajax():
        form = clasificadorform(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            data = {
                'message': 'form is saved'
                }
            return JsonResponse(data)

    context = {

        "layers":layers,
        "gps_north":gps_north,
        "gps_easting":gps_easting,
        "gps_lat":str_gps_lat,
        "gps_long":str_gps_long,
        "x":x,
        "y":y,
        "z":z,
        "form":form,
        "filename": nombre,
        "Document":document,


    }


    return render(request, 'Document/plot.html', context)


#------------------------------------------------------------------EDIT DATOS USUARIO --------------------------------------------------------------------#

def change_password(request):

    user = request.user
    form = PasswordChangeForm(request.POST or None)
    if form.is_valid():
        if request.user.check_password(form.cleaned_data['old_password']):
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            return redirect('../../')
        else:
            messages.error(request, 'La contraseña actual es errónea')


    return render(request, 'Document/edit.html',{'form':form})


def prueba(request):

    filename = '/home/hector/Aplicaciones/Django_pcl_postgresql_version2/media/documents/cloud_yaw_frame_number_953.pcd'


    pcd = read_point_cloud(filename)
    pcd_array = (np.asarray(pcd.points))

    x = []
    y = []
    z = []

    for row in pcd_array:
        x.append(float(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))



    form2 = DescriptionForm(request.POST or None)

    if form2.is_valid():
        instance = form2.save()
        instance.save()

    form = clasificadorform(request.POST or None)
    if request.is_ajax():
        form = clasificadorform(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            data = {
                'message': 'form is saved'
            }
            return JsonResponse(data)
    context = {


        "x": x,
        "y": y,
        "z": z,
        "form": form,
        "form2": form2,


    }

    return render(request, 'Document/prueba.html', context)




import json

def api_test(request):

    data = request.POST.get('http://127.0.0.1:8007/api/objects/1/')

    context =  {

                'data': data,


    }

    return render_to_response('Document/test_api.html', context)

