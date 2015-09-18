import profile
from urllib3 import request
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from rango.models import Category, Page, UserProfile
# from rango.models import Page
from rango.form import PageForm
from rango.form import CategoryForm
from rango.form import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.

def default(request):
    # define a view to disply a static homepage
    return render_to_response('rango/index.html')

@login_required
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
    category_list = Category.objects.all()
    page_list = Page.objects.order_by('views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}



    ## get cookit information
    # Get the number of visits to the website
    # We use cookie.get() function to get the visits cookie
    # If cookie exist, the value is casted to a integer
    # If the cookie doesn't exist, we default it to zero and cast that
    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False

    # Render this response and send it back
    # response = render(request, 'rango/index.html', context_dict)
    # Does the cookie last_visit_exist?
    last_visit = request.session.get('last_visit')
    if last_visit:
        # Yes it does, get the value of this cookie
        # Cast the value to a python date/time object
        # print context_dict['top_five']
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')

        # If it is been more than a day since the last visit ...
        if (datetime.now()-last_visit_time).seconds > 5:
            visits = visits + 1
            context_dict['visits'] = visits
            # ... and flag that the cookie last visit needs to be update
            reset_last_visit_time = True
        # response = render(request, 'rango/index.html', context_dict)
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set
        reset_last_visit_time = True
        # context_dict['visits'] = visits

        # Obtain our response object early so we add cookie information
        # response = render(request, 'rango/index.html', context_dict)

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
    response = render(request, 'rango/rango_index.html', context_dict)
    # Return response back to the user, updating any cookies that need changed
    return response



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

def user_registration(request):
    # Link before, get request's context
    context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == "POST":
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileForm(data=request.POST)
        # If the two forms are valid...
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        if user_form.is_valid():
            # Save the user's form data to the database.
            password = request.POST.get('password')
            email = request.POST.get('email')
            emails = User.objects.values_list('email', flat=True)
            if email in emails:
                return render_to_response('rango/registration.html', {'mail_error': "your mail is registered"}, context)
            if len(password)<4:
                pass_word_error = "your password is too short"
                return render_to_response('rango/registration.html', {'pass_word_error': pass_word_error}, context)
            else:
                user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()

             # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            # profile = profile_form.save(commit=False)
            # profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']
            # # Now we save the UserProfile model instance.
            # profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True


            return HttpResponseRedirect('/rango/')
            # return render_to_response('rango/login.html', {'messages': "test"})

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
        else:
            form_errors = user_form.errors
            # return HttpResponse(user_form.errors)

            # print form_errors
            return render_to_response('rango/registration.html', {'form_errors': form_errors}, context)
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        # profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response('rango/registration.html', {'user_form': user_form, 'registered': registered}, context)
    # return HttpResponseRedirect('/rango/')

def user_profile_update(request):
    user_id = request.user.id
    if request.method == 'GET':
        # get information from database:

        try:
            user_info = UserProfile.objects.get(user_id=user_id)
            context_dic = {'user_id':user_info.user_id, 'user_picture':user_info.picture, 'birth_day':user_info.birthday, 'website':user_info.website}
            return render(request, 'rango/user_profile_update.html', context_dic)
        except:
            return HttpResponseRedirect('/rango/user_profile_add')
    else:
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            if 'picture' in request.FILES:
                print "it is fine"
            user_profile = UserProfile.objects.get(user_id=user_id)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            profile_form.save()
            return redirect('/rango/')
        else:
            user_profile = UserProfile.objects.get(user_id=user_id)
            profile_form = UserProfileForm(instance=user_profile)
            return render_to_response('rango/user_profile_update.html', {'form':profile_form}, context_instance=RequestContext(request))
        # user_info = UserProfile.objects.get(user_id=user_id)
        # form = UserProfileForm(request.POST, instance=user_info)
        # print "test1"
        # if form.is_valid():
        #     print "test"
        #     form.save()
        # form_count = form.save(commit=False)
        # if 'picture' in request.FILES:
        #     print "test"
        #     form_count.picture = request.FILES['picture']
        # form_count.save()
        # return redirect('/rango/')

def user_profile_add(request):
    user_id = request.user.id
    context_dict ={'user_id': user_id,}
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form_count = form.save(commit=False)
            form_count.user_id = user_id
            if 'picture' in request.FILES:
                form_count.picture = request.FILES['picture']
            form_count.save()
        else:
            print messages.error(request, "error")
    # else:
    #     print "fault"
        # profiles = form.save(commit=False)
        # profiles.user_id = user_id
        # profiles.picture = request.FILES['picture']
        # profiles.website = request.POST['website']
        # profiles.birthday = request.POST['birthday']
        # profiles.save()
        # context_dict['user_id'] = user_id
        context_dict['UserProfileForm'] = form
        return render(request, 'rango/user_profile_add.html', context_dict)
    else:


        return render(request, 'rango/user_profile_add.html', context_dict)

# def user_profile_add(request):


    # # if it's a http post, we are interested in processing the form data
    # if request.method == 'POST':
    #     # Attempt to grab the information from the raw form information
    #     # Note that we make use of both userform and userprofileform
    #     user_form = UserForm(data=request.POST)
    #     profile_form = UserProfileForm(data=request.POST)
    #
    #     # If the two forms are valid ...
    #     if user_form.is_valid() and profile_form.is_valid():
    #         # Save the user's form data to the database
    #         user = user_form.save()
    #
    #         # Now, we hash the password with the set_password method
    #         # Once hashed, we can update the user object
    #         user.set_password(user.password)
    #         user.save()
    #
    #         # Now sort out UserProfile instance
    #         # Since we need to set user attribute ourselves, we set commit=False
    #         # This delay saving the model until we're ready to avoid integrity problems
    #         profile = profile_form.save(commit=False)
    #         profile.user = user
    #
    #         # Did user will provide a profile picture?
    #         # If so , we need to  get if from form and put it in the userprofile model
    #         if 'picture' in request.FILES:
    #             profile.picture = request.FILES['picture']
    #
    #         #Now we save the Userprofile model instance
    #         profile.save()
    #
    #         # Update our variable to tell the template registration was successful
    #         registered = True
    #
    #      # Invalid form or forms - mistakes or something else?
    #     # Print problems to the terminal.
    #     # They'll also be shown to the user.
    #     else:
    #         print user_form.errors, profile_form.errors
    #
    # # Not a HTTP POST, so we render our form using two ModelForm instances.
    # # These forms will be blank, ready for user input.
    # else:
    #     user_form = UserForm()
    #     profile_form = UserProfileForm()
    #
    # # Render the template depending on the context.
    # return render(request, 'rango/register.html',
    #               {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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
            context_dict["user_name"] = username
            context_dict['Password'] = password
            context_dict['bad_details'] = True
            # return HttpResponse('Invalid login details supplied')
            # return HttpResponseRedirect('/rango/login/')
            return render_to_response('rango/login.html', context_dict, context)
            # return HttpResponse("please input right user information")
    # The request is not a HTTP POST, so display login form
    # This scenario would most likely be a HTTP GET
    else:
        # No context variable to pass to the template system, hence the
        # blank dictionary object
        return render_to_response('rango/login.html', context_dict, context)


def user_logout(request):
    logout(request)
    # return HttpResponseRedirect('/rango/login/')
    return HttpResponseRedirect('/rango/login/')


# restricted access web
@login_required
def restricted(request):
    return HttpResponse("since you are logged in, you can see this text")

# User the login_required() decorator to ensure only those loged in can access the view
# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out
#     logout(request)
#
#     # Take back the user to homepage
#     return HttpResponseRedirect('/rango/')


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            print 'page_id' + page_id
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
                print url
            except:
                pass

    return redirect(url)

# def uer_profile(request):
#      user_id = request.user.id
#      print UserProfile.objects.get(user_id=user_id)

def reset_password(request):
    context_dic = {}
    context_error_dic = {}
    if request.method == "POST":
        username = request.POST.get('username')
        if username == '':
            context_error_dic['username'] = "UserName can't be blank"
        else:
            context_dic['username'] = username
        mail = request.POST.get('mail')
        try:
            validate_email(mail)
            context_dic['mail'] = mail
            print "test4"
            print context_dic
        except ValidationError:
            context_error_dic['mail'] = "Please input right mail address"
        newpassword = request.POST.get('newpassword')

        user_profile = User.objects.filter(username=username, email=mail)
        if user_profile:
            print "test"
            if newpassword == '' or len(newpassword) < 4:
                print "test1"
                context_error_dic['newpassword'] = "New password can't be blank or it is too short"
            else:
                context_dic['newpassword'] = newpassword
                user = User.objects.get(username=username, email=mail)
                user.set_password(newpassword)
                user.save()
                return redirect('/rango/login')
        else:
            context_error_dic['form_error'] = 'your information is not right'
            return render_to_response('rango/passwd_reset.html', context_error_dic, RequestContext(request))

    return render_to_response('rango/passwd_reset.html', context_error_dic, RequestContext(request))
