import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango.settings')

import django

django.setup()

from rango.models import Category, Page


def populate():
    python_cat = add_cat('Python')

    add_page(cat=python_cat,
             title='How to THink like a Computer Scientist',
             url="http://www.greenteapress.com/thinkpython/",
             views=9)
    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/",
             views=1)
    add_page(cat=python_cat,
             title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/",
             views=3)

    django_cat = add_cat("Django")

    add_page(cat=django_cat,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/",
             views=8)

    add_page(cat=django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/",
             views=10)

    add_page(cat=django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/",
             views=11)

    frame_cat = add_cat("Other Frameworks")

    add_page(cat=frame_cat,
             title="Bottle",
             url="http://bottlepy.org/docs/dev/",
             views=12)

    add_page(cat=frame_cat,
             title="Flask",
             url="http://flask.pocoo.org",
             views=6)

    home_cat = add_cat("Home")

    add_page(cat=home_cat,
             title="furniture for home",
             url="www.ikea.com.cn",
             views=7)

    # Print out what we have added to the user
    for c in Category.objects.all():
        for p in Page.objects.filter(Category=c):
            print "-{0}-{1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(Category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    if name == "Python":
        c.views = 128
        c.likes = 64
        #c.save()
    if name == "Django":
        c.views = 64
        c.likes = 32
    if name == "Other Frameworks":
        c.views = 32
        c.likes = 16
    c.save()
    return c

# execute from here

if __name__ == '__main__':
    print "Startting Rango population script ....."
    populate()