from django.shortcuts import render
from rango.models import Category
from rango.models import Page

from rango.form import CategoryForm
# Create your views here.

def index(request):
    ## this version for first index page
    # #Contruct a dictionary to pass to template engine as its context.
    # #Note the key boldmessage is the same as {{boldmessage}} in the template
    # context_dict = {'blodmessage': 'I am bold font from the context'}
    #
    # # Return a rendered response to send to client.
    # # We make use of the shortcut function to make our live easier.
    # # Not the first parameter is the template we wish to use
    # return render(request, 'rango/index.html', context_dict)

    ### this version is for second index page
    # Query the database for a list for all categories currently stored
    # Order this category by no. likes in descending order
    # Retrieve the top 5 only -- or all if less than 5
    # Place the list in our context dictionary which will pass to the template engine
    category_list = Category.objects.order_by('-likes')[:5]
    page_top_five_list = Page.objects.order_by('views')[:5]
    context_dict = {'categories': category_list}
    context_dict['top_five'] = page_top_five_list
    # Render this response and send it back
    return render(request, 'rango/index.html', context_dict)


def about(request):
    # change about page from static file to template file
    return render(request, 'rango/about.html')

def category(request, category_name_slug):
    # Create a context dictionary which we can pass to template rendering engine
    context_dict = {}

    try:
        # can find a category name slug with the given name?
        # If we can't, the .get() method raise a DoesNotExist exception
        # So the .get() method return one model instance or raises a exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all associated pages.
        # Note that filter return >= 1 model instance.
        pages = Page.objects.filter(Category=category)

        # Add our results list to the template context under name pages.
        context_dict['pages'] = pages

        # We also add category objects from database to the context dictionary
        # we'll use this in the template to verify that category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get there if we didn't find the specified category
        # Doesn't do anything - the template display the "no category" message for us
        pass
    # Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)


def add_category(request):

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provide with a valid form?
        if form.is_valid():
            # save this new category into the database
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the hompage
            return index(request)
        else:
            # The supplied form contained errors - just print them on the terminal
            print form.errors

    else:
        # If the request was not a Post, display the form to enter details.
        form = CategoryForm()

    # Bad form(or form details), no form supplied...
    # Render the form with error message (if any)...
    return render(request, 'rango/add_category.html', {'form': form})
