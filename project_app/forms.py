from django import forms
from .models import Space


class AddSpace(forms.ModelForm):

    img=forms.ImageField()    #save image as blob
    email = forms.EmailField(widget = forms.HiddenInput())
    capacity = forms.CharField(max_length=1000)
    # telephone = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'placeholder': '*Telephone..'}))
    address = forms.CharField(max_length=100, required=True)
    comments=forms.CharField(max_length=1000)
    class Meta:
        model = Space
        fields = ('img','email','capacity','address','comments')
