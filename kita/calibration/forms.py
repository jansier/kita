from django import forms

class CalibrateMapForm(forms.Form):
    map_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'image/tif,image/tiff'}))
    p1x = forms.IntegerField(label='Point 1 X')
    p1y = forms.IntegerField(label='Point 1 Y')
    p2x = forms.IntegerField(label='Point 2 X')
    p2y = forms.IntegerField(label='Point 2 Y')
    p3x = forms.IntegerField(label='Point 3 X')
    p3y = forms.IntegerField(label='Point 3 Y')
    p4x = forms.IntegerField(label='Point 4 X')
    p4y = forms.IntegerField(label='Point 4 Y')