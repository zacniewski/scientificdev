from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'What to look for?',
                'class': 'form-control search-field round',
                'type': 'search',
            }
        )
    )
