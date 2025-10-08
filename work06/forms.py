from django import forms


class ReiwaForm(forms.Form):
    reiwa_year = forms.IntegerField(label="令和何年ですか？", min_value=1)
