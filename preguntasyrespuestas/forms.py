from django import forms

class PostForm(forms.Form):
    asunto = forms.CharField(max_length=200)
    descripcion = forms.CharField(widget=forms.Textarea)


class PostFormRta(forms.Form):
    contenido = forms.CharField(max_length=200)
    mejor_respuesta = forms.BooleanField(required=False)
