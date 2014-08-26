from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
# Import the Category model
from bookmark.models import Category
from bookmark.models import Page
from bookmark.forms import PageForm

def decode_url(url):
    return url.replace(' ', '_')
  
def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query for categories - add the list to our context dictionary.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Render the response and return to the client.
    return render_to_response('bookmark/index.html', context_dict, context)
  
  
def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = category_name_url.replace('_', ' ')
    category_url_name = category_name.replace(' ', '_')
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name}
    context_dict['category_url_name'] = category_url_name
    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('bookmark/category.html', context_dict, context)
  
from bookmark.forms import CategoryForm

def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('bookmark/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
  context = RequestContext(request)
  
  category_name = category_name_url.replace(' ', '_')
  context_dict = {'category_name': category_name}
  category_name_ref = category_name.replace('_',' ')
  
  try:
    category = Category.objects.get(name=category_name_ref)
    context_dict['category'] = category
    
  except Category.DoesNotExist:
    return render_to_response('bookmark/error.html', {}, context)
      
  if request.method == 'POST':
    page = PageForm(request.POST)
    if page.is_valid():
      savedstate = page.save(commit=False)
      savedstate.category = Category.objects.get(name=category_name_url)
      savedstate.views = 0
      savedstate.save()
      page.save_m2m()
      
      return index(request)
    else:
      print page.errors
      
  else:
    page = PageForm()
    '''if page.is_valid():
      print("SHI")
      savedstate = page.save(commit=False)
      savedstate.category = Category.objects.get(name=category_name_url)
      savedstate.views = 0
      savedstate.save()
      page.save_m2m()
      
      return index(request)
    else:
      print page.errors'''
  
  context_dict['page'] = page
  
  return render_to_response('bookmark/add_page.html', context_dict, context)