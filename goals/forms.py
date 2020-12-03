from django import forms

from .models import Goal, User, Profile


class GoalForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=GoalCategories.objects.values('name'))
    deadline = forms.DateField(widget=(forms.DateInput(format='%m/%d/%Y', attrs={"class": "form-control", "id": "datepicker"})))
    amount = forms.DecimalField(min_value=0, max_value=1000000, decimal_places=2),

    class Meta:
        model = Goal
        fields = ['title', 'description', 'category', 'amount', 'term', 'deadline', 'purpose']
        labels = {'deadline': 'Accomplish this Goal by:'}

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=(forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'id': 'datepicker'})))
    class Meta:
        model = Profile
        fields = ['profile_picture', 'date_of_birth',]
        labels = {'date_of_birth': 'Date of birth'}