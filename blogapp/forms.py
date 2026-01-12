from django import forms
from .models import Review




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Review Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Review Content'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }
