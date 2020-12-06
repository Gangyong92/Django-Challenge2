from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            "text",
            "rating",
        )

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full h-2/3 border outline-none shadow py-2 px-2 mb-1",
                "placeholder": "Write review ~",
            }
        ),
    )

    rating = forms.IntegerField(
        max_value=5,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full h-1/3 border shadow",
                "placeholder": "Rating: 1 ~ 5",
            }
        ),
    )

    def save(self):
        review = super().save(commit=False)
        return review