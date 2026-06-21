from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'priority': forms.Select(choices=Task._meta.get_field('priority').choices),
            'category': forms.Select(choices=Task._meta.get_field('category').choices),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters.")
        return title

# from django import forms
# from .models import Task

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'due_date', 'priority','category']  # Specify which fields of the Task model to use in the form
#         widgets = {
#             'due_date': forms.DateInput(attrs={'type': 'date'}),
#             'priority': forms.Select(choices=Task._meta.get_field('priority').choices),
#             'category': forms.Select(choices=Task._meta.get_field('category').choices),
#         }
