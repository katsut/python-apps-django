from django import forms
from .models import Todo


class TodoCreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "due_date"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "タスク名を入力してください",
                }
            ),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"].required = False


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "due_date", "is_completed"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "タスク名を入力してください",
                }
            ),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"].required = False
