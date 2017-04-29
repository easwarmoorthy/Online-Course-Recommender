from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from math import sqrt
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



def pearson_correlation(person1,person2):
	person1 = CoursereviewModel.objects.all().filter(user_id = person1)
	person2 = CoursereviewModel.objects.all().filter(user_id = person2.id)
	# To get both rated items
	both_rated1,both_rated2 = {},{}
	for item in person1:
		for x in person2:
			if item.course == x.course:
				both_rated1[item] = 1
				both_rated2[x] = 1
	number_of_ratings = len(both_rated1)

	# Checking for number of ratings in common
	if number_of_ratings == 0:
		return 0

	# Add up all the preferences of each user
	person1_preferences_sum,person2_preferences_sum = 0,0
	person1_square_preferences_sum,person2_square_preferences_sum = 0,0
	for item in both_rated1:
		person1_preferences_sum +=item.rating
		person1_square_preferences_sum +=item.rating*item.rating
	for item in both_rated2:
		person2_preferences_sum +=item.rating
		person2_square_preferences_sum +=item.rating*item.rating
	print person1_preferences_sum
	print person2_preferences_sum

	# Sum up the squares of preferences of each user


	print person1_square_preferences_sum
	print person2_square_preferences_sum

	# Sum up the product value of both preferences for each item
	product_sum_of_both_users = 0
	for item in person1:
		for x in person2:
			if x.course != item.course:
				product_sum_of_both_users += x.rating*item.rating
	print product_sum_of_both_users
	# Calculate the pearson score
	numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
	denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
	if denominator_value == 0:
		return 0
	else:
		r = numerator_value/denominator_value
		return r

def recommendation(request):
	try:
		if request.session['member_id']:
			userkey = request.session['member_id']
			person = CoursereviewModel.objects.filter(user_id = userkey)
			other_persons = User.objects.all()
			# Gets recommendations for a person by using a weighted average of every other user's rankings
			totals = {}
			simSums = {}
			rankings_list =[]
			for other in other_persons:
				if other == person:
					continue
				sim = pearson_correlation(userkey,other)

				print "works",sim
				if sim <=0:
					continue
				other_data = CoursereviewModel.objects.all().filter(user_id = other.id)
				print other_data,"\n",person
				for item in other_data:
					find = False
					for x in person:
						if item.course_id == x.course_id:
							find = True
						if(not find):
							totals.setdefault(item,0)
							totals[item] += item.rating* sim
							# sum of similarities
							simSums.setdefault(item,0)
							simSums[item]+= sim

			rankings = [(total/simSums[item],item) for item,total in totals.items()]
			rankings.sort()
			rankings.reverse()
			# returns the recommended items
			recommendations_list = [recommend_item for score,recommend_item in rankings]
			list2 = []
			for x in recommendations_list:
				list2.append(x.course)
			list2 = list(set(list2))
			for item in list2:
				for item.course in person:
					pass
			res_list = list2
			paginator = Paginator(res_list, 7) # Show 25 contacts per page
			page = request.GET.get('page')
			try:
			    list1 = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			    list1 = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			    list1= paginator.page(paginator.num_pages)
			context = {"list1":list1}
			return render(request, "course/all.html", context)
			# Sort the similar persons so that highest scores person will appear at the first
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})



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
			return HttpResponseRedirect('/all/')
		else:
			return render(request, "course/form.html", context)
	return render(request, "course/form.html", context)

def rating_view(request,pk):
	userkey = request.session['member_id']
	rating = 0
	edit = False
	try:
		user =  User.objects.filter(id = userkey)[0]
		course = CourseModel.objects.filter(id = pk)[0]
		my_record= {"label":""}
		one,two,three,four,five = "","","","",""
		d = CoursereviewModel.objects.all().filter(user_id = user.id)
		for x in d:
			if str(x.course_id) == str(pk):
				edit = True
				my_record["label"] = x.review
				rating = x.rating
	except IndexError:
		pass
	searchform = SearchForm(request.POST or None,initial = { 'label':my_record})
	list2 = CourseModel.objects.all()
	#my_record = CoursereviewModel.objects.filter(user = userkey)[0].course.objects.filter(id = pk)[0]
	print my_record,searchform.is_valid()
	try:
		if request.session['member_id']:
			if searchform.is_valid() and not edit:
				rating = int(request.POST.get("rating"))
				keyword = searchform.cleaned_data.get("keyword")
				data_list = CoursereviewModel()
				data_list.user =  User.objects.filter(id = userkey)[0]
				data_list.rating = rating
				data_list.review = keyword
				data_list.course = CourseModel.objects.filter(id = pk)[0]
				data_list.save()
				res_list = CourseModel.objects.all()
				paginator = Paginator(res_list, 10) # Show 25 contacts per page
				page = request.GET.get('page')
				list2 =  []
				try:
				    list1 = paginator.page(page)
				except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				    list1 = paginator.page(1)
				except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				    list1= paginator.page(paginator.num_pages)
				context = {"list1":list1}
				return HttpResponseRedirect('/all/')
			elif searchform.is_valid():
				rating = int(request.POST.get("rating"))
				user =  User.objects.filter(id = userkey)[0]
				course = CourseModel.objects.filter(id = pk)[0]
				d = CoursereviewModel.objects.all().filter(user_id = user.id)
				keyword = searchform.cleaned_data.get("keyword")
				for x in d:
					print x.course_id
					if str(x.course_id) == str(pk):
						print type(keyword),type(x.review)
						x.review = keyword
						CoursereviewModel.objects.all().filter(user_id = user.id).filter(course_id = pk).update(review = keyword,rating = rating)
				res_list = CourseModel.objects.all()
				paginator = Paginator(res_list, 10) # Show 25 contacts per page
				page = request.GET.get('page')
				list2 =  []
				try:
				    list1 = paginator.page(page)
				except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				    list1 = paginator.page(1)
				except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				    list1= paginator.page(paginator.num_pages)
				context = {"list1":list1}
				return HttpResponseRedirect('/all/')
		context = {"list2":list2,"form":searchform}
		return render(request, "course/rating.html", context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})


def allcourse_view(request):
	list1 = CourseModel.objects.all()
	context = {"list1":list1}
	try:
		if request.session['member_id']:
			res_list = CourseModel.objects.all()
			paginator = Paginator(res_list, 10) # Show 25 contacts per page
			page = request.GET.get('page')
			list2 =  []
			try:
			    list1 = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			    list1 = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			    list1= paginator.page(paginator.num_pages)
			context = {"list1":list1}
			return render(request, "course/all.html", context)
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
		return HttpResponseRedirect('/all/')
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
