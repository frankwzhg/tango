
from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="please enter your category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)


    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between the modelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="please enter page title of the page")
    url = forms.URLField(max_length=200, help_text="please enter the URL of this page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # what fields do we want to include in our form?
        # This way we don't need every field in the model form present.
        # Some fields allow NULL values, so we may not want to include them ....
        # Here, we are hiding the foreign key.
        # We can either exclude the category field from the form.
        exclude = ('Category',)

        # Or, for special the fields to include(i.e. not include the category field)
        #fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # if url is empty or doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'birthday')


class ChangePicForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

# class ChangePasswordForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('password',)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

# Clean email field
def clean_email(self):
    email = self.cleaned_data["email"]
    try:
        User._default_manager.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError('duplicate email')

# modify save() method so that we can set user.is_active to False when we first create our user
def save(self, commit = True):
    user = super(RegistrationForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.is_active = False
        user.save()
    return user