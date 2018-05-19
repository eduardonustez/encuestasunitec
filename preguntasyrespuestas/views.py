from django.http import HttpResponse
from preguntasyrespuestas.models import Pregunta
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.shortcuts import render
from django.utils import timezone
from preguntasyrespuestas.forms import PostForm, PostFormRta
from django.contrib.auth.models import Permission


def index(request):
   return HttpResponse("Pagina de inicio")

def basePreguntas(request):
    preguntas = Pregunta.objects.all()
    #respuesta_string = "<h1> Base de Preguntas </h1>"
    #respuesta_string += "<br/>".join(["id: %s, asunto: %s" %(p.id,p.asunto) for p in preguntas])
    #return HttpResponse(respuesta_string)
    context ={'lista_preguntas':preguntas}
    return render(request, "preguntas.html", context)

def Pregunta_Detalle(request,pregunta_id):
    pregunta = Pregunta.objects.get(pk=pregunta_id)
    preg_sig = pregunta.id + 1
    context = {'pregunta': pregunta,'preg_sig':preg_sig}
    return render(request, "pregunta_detalle.html", context)

def crear_pregunta(request):
 #si es una peticion post
    if request.user.is_authenticated() and request.user.has_perm('preguntasyrespuestas.add_pregunta'):
        agregar_respuesta = 0
        Id_NuevaPregunta = 0
        if request.method == "POST":
    	    #asignamos a form el formulario para validar
            form = PostForm(request.POST)
            #si el formulario es validado correctamente
            if form.is_valid():
        	    #creamos una nueva instancia de Post con los campos del form
        	    #asi capturamos los valores post
        	    newPregunta = Pregunta(asunto = request.POST["asunto"], descripcion = request.POST["descripcion"],fecha_publicacion=timezone.now())
        	    #guardamos el post11
        	    newPregunta.save()
            Id_NuevaPregunta=newPregunta.id
            agregar_respuesta = 1
        	    #redirigimos a la ruta con name add_post, que es esta
            #	return redirect('add_pregunta')
        else:
    	    #si no es una peticion post, asignamos a form
    	    #el form que hemos creado sin datos
            form = PostForm()

            #siempre devolvemos la misma respuesta
            #return render_to_response("pregunta.html",{"form":form}, context_instance = RequestContext(request))
            return render(request, 'pregunta.html', {'form': form,'agregar_respuesta':agregar_respuesta,'Id_NuevaPregunta':Id_NuevaPregunta})
    else:
        return HttpResponse("Usted no esta autorizado para esta operacion.")

def crear_respuesta(request,pregunta_id):
 #si es una peticion post
    if request.method == "POST":
    	#asignamos a form el formulario para validar
        form = PostFormRta(request.POST)
        #si el formulario es validado correctamente
        if form.is_valid():
            booRta = False
            if request.POST["mejor_respuesta"]:
                booRta = True

            pregunta = Pregunta.objects.get(pk=pregunta_id)
            pregunta.respuesta_set.create(contenido=request.POST["contenido"], mejor_respuesta=booRta)
    else:
    	#si no es una peticion post, asignamos a form
    	#el form que hemos creado sin datos
        form = PostFormRta()
    return render(request, 'nueva_respuesta.html', {'form': form})