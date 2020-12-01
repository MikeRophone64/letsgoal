from django import forms

from .models import Goal


class GoalForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=GoalCategories.objects.values('name'))
    deadline = forms.DateField(widget=(forms.DateInput(format='%m/%d/%Y', attrs={"class": "form-control", "id": "datepicker"})))
    amount = forms.DecimalField(min_value=0, max_value=1000000, decimal_places=2),

    class Meta:
        model = Goal
        fields = ['title', 'description', 'category', 'amount', 'term', 'deadline', 'purpose']
        labels = {'deadline': 'Accomplish this Goal by:'}
        # widgets = {
        #     'title': forms.TextInput(attrs={"class": "form-control"}),
        #     'description': forms.Textarea(attrs={"class": "form-control"}),
        #     'category': forms.Select(attrs={"class": "form-control"}),
        #     'term': forms.Select(attrs={"class": "form-control"}),
        #     # 'deadline': forms.DateInput(attrs={"class": "form-control", "id": "datepicker"}),
        #     'purpose': forms.Textarea(attrs={"class": "form-control"}),
        #     }