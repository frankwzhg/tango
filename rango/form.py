from django import forms
from rango.models import Page, Category

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