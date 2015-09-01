import profile
from urllib3 import request
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from rango.models import Category
from rango.models import Page
from rango.form import PageForm
from rango.form import CategoryForm
from rango.form import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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

@login_required
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

@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
        print cat.id

    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form .is_valid():
            if cat:
                page = form.save(commit=False)
                page.Category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors

    else:
        form = PageForm()
    context_dic = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}

    return render(request, 'rango/add_page.html', context_dic)

def register(request):
    # A boolean value for telling template whether the registration was successful
    # Set it to False initially, program change it's value to True when registration succeed
    registered = False

    # if it's a http post, we are interested in processing the form data
    if request.method == 'POST':
        # Attempt to grab the information from the raw form information
        # Note that we make use of both userform and userprofileform
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid ...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now, we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out UserProfile instance
            # Since we need to set user attribute ourselves, we set commit=False
            # This delay saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user will provide a profile picture?
            # If so , we need to  get if from form and put it in the userprofile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we save the Userprofile model instance
            profile.save()

            # Update our variable to tell the template registration was successful
            registered = True

         # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    context = RequestContext(request)
    context_dict = {}
    # If this request is http post, try to pull out the relevant information
    if request.method == 'POST':
        # Gather username and password provided by user
        # This information is obtained from the login form
            # We use request.POST.get(<variable>) as opposed to request.POST['<variable>'],
            # because the request.POST.get(<variable>)return None, if the value does not exist
            # While the request.POST(<variable>) will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use django's machinery to attempt to see if username/password
        # combination is valide - a user object is returned if it is
        user = authenticate(username=username, password=password)

        # If we have a user object, the details are correct
        # If None( Python's way of representing the absence of a value), no user
        # with matching credentials was found
        if user is not None:
            # is the account is active? it can have been disable.
            if user.is_active:
                # If the account is valid and active, we can log the user in
                # We can send this user back to homepage
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in
                context_dict['disableed_account'] = True
                return HttpResponse("Your rango's account is disable")
        else:
            # Bad login details were provide, So we can't log the user in
            print "invalide login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            # return HttpResponse('Invalid login details supplied')
            # return HttpResponseRedirect('/rango/login/')
            return render_to_response('rango/login.html', context_dict, context)
    # The request is not a HTTP POST, so display login form
    # This scenario would most likely be a HTTP GET
    else:
        # No context variable to pass to the template system, hence the
        # blank dictionary object
        return render_to_response('rango/login.html', context_dict, context)

# restricted access web
@login_required
def restricted(request):
    return HttpResponse("since you are logged in, you can see this text")

# User the login_required() decorator to ensure only those loged in can access the view
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out
    logout(request)

    # Take back the user to homepage
    return HttpResponseRedirect('/rango/')
