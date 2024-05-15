from .profile import *
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from os import name
from django.db.models.query import QuerySet
from django.forms import fields
from django.forms.models import ModelForm
from django.forms.widgets import FileInput , RadioSelect
from.models import Rating, User, Question , InstantAdvice


gender = [
    ('male', 'male'),
    ('female', 'female')

]

rate = [
    ('rate1', '1'),
    ('rate2', '2'),
    ('rate3', '3'),
    ('rate4', '4'),
    ('rate5', '5')



]


class AdvocateSignupForm(UserCreationForm):
    mobile = forms.CharField(min_length=10 ,required=True )

    class Meta:
        model = User
        fields = ('name',  'email',  'city', 'password1', 'password2'  , 'mobile')

    def __init__(self, *args, **kwargs):
        super(AdvocateSignupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update( {'required': True, 'name': 'name', 'id': 'name', 'class': 'form-control1', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update( {'required': True, 'name': 'email', 'id': 'email', 'class': 'form-control1 signup_input', 'placeholder': 'Email'}),
        self.fields['city'].widget.attrs.update( {'name': 'city', 'id': 'city', ' class': 'form-control1 signup_input', 'placeholder': 'City'})
        self.fields['password1'].widget.attrs.update( {'name': 'password1', 'id': 'password1', 'class': 'form-control1 signup_input', 'placeholder': 'Password'}),
        self.fields['password2'].widget.attrs.update( {'name': 'password2', 'id': 'password2', 'class': 'form-control1 signup_input', 'placeholder': 'Confirm Password'})
        self.fields['mobile'].widget.attrs.update( {'name': 'mobile', 'id': 'mobile', 'class': 'form-control1 signup_input', 'placeholder': 'Mobile'})


class DateInput1(forms.DateInput):
    input_type = 'date'


class DateInput2(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):

    gender = forms.ChoiceField( choices=gender, widget=forms.RadioSelect, required=False)
    class Meta:
        model = AdvocateProfile
        fields = ('dob', 'gender',  'pincode', 'state', 'address', 'language_spoken', 'practicing_since',  'enrollment_number', 'bio')
        widgets = {
            'practicing_since': DateInput1(),
            'dob': DateInput2(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['gender'].widget.attrs.update(  {'required': False, 'type': 'radio', 'choices': gender}),
        self.fields['state'].widget.attrs.update({'required': False, 'class': 'form-control1 '}),
        self.fields['dob'].widget.attrs.update({'required': False, 'class': 'form-control1'}),
        self.fields['address'].widget.attrs.update({'required': False, 'class': 'form-control '}),
        self.fields['pincode'].widget.attrs.update(  {'required': False, 'class': 'form-control1 '}),
        self.fields['language_spoken'].widget.attrs.update(   {'required': False, 'class': 'form-control1 '}),
        self.fields['practicing_since'].widget.attrs.update(   {'required': False, 'class': 'form-control1 '}),
        self.fields['enrollment_number'].widget.attrs.update(   {'required': False, 'class': 'form-control1 '}),
        # self.fields['mobile'].widget.attrs.update(   {'required': False, 'class': 'form-control1'}),

        self.fields['bio'].widget.attrs.update( {'required': False, 'class': 'form-control '}),
       

class edit_user_form(forms.ModelForm):

    email = forms.EmailField(disabled=True)
    image = forms.ImageField(widget=FileInput, required=False)
    mobile = forms.CharField(min_length=10 ,required=False ,disabled = True )

    class Meta:
        model = User
        fields = ('name', 'email', 'city','image' , 'mobile')

    def __init__(self, *args, **kwargs):
        super(edit_user_form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'required': True, 'name': 'email', 'id': 'email', 'class': 'form-control1 signup_input'}),
        self.fields['name'].widget.attrs.update({'required': False, 'name': 'name', 'id': 'name', 'class': 'form-control1 signup_input'})
        self.fields['city'].widget.attrs.update({'required': False,  'name': 'city', 'id': 'city', ' class': 'form-control1 signup_input'})
        self.fields['image'].widget.attrs.update( {'required': False, 'class': 'text-file'  ,'onchange':'fun(this)' , }),


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationModel
        fields = {'course_name', 'college_name'}

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)

        self.fields['college_name'].widget.attrs.update( {'class': 'form-control1 '}),
        self.fields['course_name'].widget.attrs.update( {'class': 'form-control1 '}),


class CaseForm(forms.ModelForm):
    class Meta:
        model = CaseProfile
        fields = {'case_title', 'case_year', 'case_law', 'case_description'}
        widgets = {
            'case_year': DateInput1(),
        }

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)

        self.fields['case_title'].widget.attrs.update( {'class': 'form-control1 '}),
        self.fields['case_year'].widget.attrs.update( {'class': 'form-control1 '}),
        self.fields['case_law'].widget.attrs.update({'class': 'form-control1 '}),
        self.fields['case_description'].widget.attrs.update( {'class': 'form-control1 ', 'rows': '3'}),


class UserSignupForm(UserCreationForm):
    mobile = forms.CharField(min_length=10 ,required=True )

    class Meta:
        model = User
        fields = ('name',  'email',  'city', 'password1', 'password2' , 'mobile')

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update( {'required': True, 'name': 'name', 'id': 'name', 'class': 'form-control1 signup_input', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update( {'required': True, 'name': 'email', 'id': 'email', 'class': 'form-control1 signup_input', 'placeholder': 'Email'}),
        self.fields['city'].widget.attrs.update( {'name': 'city', 'id': 'city', ' class': 'form-control1 signup_input', 'placeholder': 'City'})
        self.fields['password1'].widget.attrs.update( {'name': 'password1', 'id': 'password1', 'class': 'form-control1 signup_input', 'placeholder': 'Password'}),
        self.fields['password2'].widget.attrs.update( {'name': 'password2', 'id': 'password2', 'class': 'form-control1 signup_input', 'placeholder': 'Confirm Password'})
        self.fields['mobile'].widget.attrs.update( {'name': 'mobile', 'id': 'mobile', 'class': 'form-control1 signup_input', 'placeholder': 'mobile'})


class UserProfileform(forms.ModelForm):

    gender = forms.ChoiceField( choices=gender, widget=forms.RadioSelect, required=False)
    mobile = forms.CharField(min_length=10 , required = False ,disabled = True  )
    class Meta:
        model = UserProfile
        fields = ['state', 'pincode', 'mobile','address', 'dob', 'gender' ]
        widgets = {

            'dob': DateInput2(),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileform, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update( {'required': False, 'type': 'radio', 'choices': gender}),
        self.fields['state'].widget.attrs.update( {'required': False, 'class': 'form-control1 '}),
        self.fields['dob'].widget.attrs.update({'required': False, 'class': 'form-control1'}),
        self.fields['address'].widget.attrs.update({'required': False, 'class': 'form-control1', 'cols': '50', "rows": '1'}),
        self.fields['pincode'].widget.attrs.update( {'required': False, 'class': 'form-control1'}),
        self.fields['mobile'].widget.attrs.update( {'name': 'mobile', 'id': 'mobile', 'class': 'form-control1 ', 'placeholder': 'Mobile'}),


# class QuetionForm(forms.ModelForm):

#     date = forms.DateField(required=False)
#     class Meta:
#         model = Quetion
#         fields = ['title' , 'quetion_description' , 'area_of_law']


#     def __init__(self, *args, **kwargs):
#         super(QuetionForm, self).__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs.update({ 'required': False, 'class' : 'form-control1' , 'placeholder':'Title'}),
#         self.fields['area_of_law'].widget.attrs.update({ 'required': False, 'class' : 'form-control1 ', 'placeholder':'Area Of Law' }),

#         self.fields['quetion_description'].widget.attrs.update({ 'required': False, 'style':'max-width:100%', 'placeholder':'Description' }),



class AdviceForm(forms.ModelForm):
    mobile = forms.CharField(min_length=10)
    class Meta:
        model = InstantAdvice
        fields = ['name','mobile','advocate']

    def __init__(self, *args, **kwargs):
        super(AdviceForm, self).__init__(*args, **kwargs)
        self.fields['advocate'].widget.attrs.update({ 'required': True,'placeholder':'Title'}),
        