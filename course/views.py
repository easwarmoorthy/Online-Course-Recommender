from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .models import *
from .forms import *
def index(request):
	return render(request,"course/index.html")

def login_view(request):
	form = UserLoginForm(request.POST or None)
	title = "Login"
	list1=""
	context = {"form":form ,"list1":list1,"title":title}
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request,user)
		request.session['member_id'] = user.id
		if user.is_authenticated():
			list1 = CourseModel.objects.all()
			context = {"form":form ,"list1":list1,"title":title}
			return render(request, "course/all.html", context)
		else:
			return render(request, "course/form.html", context)
	return render(request, "course/form.html", context)

def rating_view(request,pk):
	searchform = SearchForm(request.POST or None)
	list2 = CourseModel.objects.get(pk=pk)
	try:
		if request.session['member_id']:
			if searchform.is_valid():
				keyword = searchform.cleaned_data.get("keyword")
				list1 = CourseModel.objects.all()
				context = {"list1":list1}
				return render(request, "course/all.html", context)
		context = {"list2":list2,"form":searchform}
		return render(request, "course/rating.html", context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})


def allquotes_view(request):
	list1 = CourseModell.objects.all()
	context = {"list1":list1}
	try:
		if request.session['member_id']:
			return render(request,"course/all.html",context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})

def quote_view(request):
	#form = MyModelForm(instance=my_record)
	form = QuoteForm(request.POST or None)
	msg = None
	try:
		if request.session['member_id']:
			if form.is_valid():
				quote = form.cleaned_data["quote"]
				qname = form.cleaned_data["qname"]
				new_quote = form.save(commit=False)
				new_quote.user_id = request.session['member_id']
				new_quote.save()
				msg = {"quote":quote,"qname":qname}
			context = {"form":form,"msg":msg}
			return render(request,"course/quote.html",context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})

def edit_view(request,pk):
	my_record = CourseModel.objects.get( id = pk)
	#form = MyModelForm(instance=my_record)
	form = QuoteForm(request.POST or None,instance=my_record)
	msg = None
	try:
		if request.session['member_id']:
			if form.is_valid():
				quote = form.cleaned_data["quote"]
				qname = form.cleaned_data["qname"]
				#Entry.objects.filter(pub_date__year=2010).update(comments_on=False, headline='This is old')
				CourseModel.objects.filter(id = pk).update(quote=quote,qname = qname)
				#CourseModel.objects.filter(pk=quote.pk).update(active=True)
				msg = {"quote":quote,"qname":qname}
				print msg
			context = {"form":form,"msg":msg}
			return render(request,"course/quote.html",context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})

def delete_view(request,pk):
	my_record = CourseModel.objects.filter( id = pk).delete()
	cuser = request.session['member_id']
	x = User.objects.get(id = cuser)
	title = x.username
	list1 = CourseModel.objects.all().filter( user__username = x.username)
	context = {"list1":list1}
	try:
		if request.session['member_id']:
			return render(request,"course/userpage.html",context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})

def user_view(request):
	cuser = request.session['member_id']
	x = User.objects.get(id = cuser)
	title = x.username
	list1 = CourseModel.objects.all().filter( user__username = x.username)
	print list1
	context = {"list1":list1,"title":title}
	return render(request,"course/userpage.html",context)

def searchview(request):
    searchform = SearchForm(request.POST or None)
    try:
	    if request.session['member_id']:
		    if searchform.is_valid():
		        keyword = searchform.cleaned_data.get("keyword")
		        list1 = CourseModel.objects.all().filter( qname__contains = keyword )
		        context = {"list1":list1}
		        return render(request, "course/search.html", context)
		    context = {"searchform":searchform}
		    return render(request, "course/search.html", context)
    except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})

def register_view(request):
	form = UserRegisterForm(request.POST or None)
	title = "Register"
	list1 = None
	if form.is_valid():
		user = form.save(commit = False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		login(request,user)
		list1 = CourseModel.objects.all()
		context = {"form":form ,"list1":list1,"title":title}
		return render(request, "course/all.html", context)
	context = {"form":form ,"list1":list1,"title":title}
	return render(request,"course/form.html",{"form":form})

def logout_view(request):
	print logout(request)
	try:
		del request.session['member_id']
	except KeyError:
		pass
	form = "Logged out successfully"
	return render(request,"course/index.html",{"form":form})

# Create your views here.
