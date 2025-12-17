from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "email", "commentText"]
        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "commentText": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        labels = {
            "commentText": "Комментарий",
        }

    def clean_body(self):
        body = self.cleaned_data.get("body", "")
        if len(body.strip()) == 0:
            raise forms.ValidationError("Комментарий не может быть пустым.")
        return body
