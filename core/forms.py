from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-box',
            'placeholder': 'Search...'
        })
    )