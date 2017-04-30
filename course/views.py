from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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

def pearson_correlation(person1,person2):
	person1 = CoursereviewModel.objects.all().filter(user_id = person1)
	person2 = CoursereviewModel.objects.all().filter(user_id = person2.id)
	both_rated1,both_rated2 = {},{}
	for item in person1:
		for x in person2:
			if item.course == x.course:
				both_rated1[item] = 1
				both_rated2[x] = 1
	number_of_ratings = len(both_rated1)
	if number_of_ratings == 0:
		return 0
	person1_preferences_sum,person2_preferences_sum = 0,0
	person1_square_preferences_sum,person2_square_preferences_sum = 0,0
	for item in both_rated1:
		person1_preferences_sum +=item.rating
		person1_square_preferences_sum +=item.rating*item.rating
	for item in both_rated2:
		person2_preferences_sum +=item.rating
		person2_square_preferences_sum +=item.rating*item.rating
	product_sum_of_both_users = 0
	for item in person1:
		for x in person2:
			if x.course != item.course:
				product_sum_of_both_users += x.rating*item.rating
	numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
	denominator_value = sqrt((person1_square_preferences_sum - \
	pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum - \
	pow(person2_preferences_sum,2)/number_of_ratings))
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
			totals = {}
			simSums = {}
			rankings_list =[]
			for other in other_persons:
				if other == person:
					continue
				sim = pearson_correlation(userkey,other)
				if sim <=0:
					continue
				other_data = CoursereviewModel.objects.all().filter(user_id = other.id)
				for item in other_data:
					find = False
					for x in person:
						if item.course_id == x.course_id:
							find = True
						if(not find):
							totals.setdefault(item,0)
							totals[item] += item.rating* sim
							simSums.setdefault(item,0)
							simSums[item]+= sim
			rankings = [(total/simSums[item],item) for item,total in totals.items()]
			rankings.sort()
			rankings.reverse()
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
			    list1 = paginator.page(1)
			except EmptyPage:
			    list1= paginator.page(paginator.num_pages)
			context = {"list1":list1,"title":"Recommedations"}
			return render(request, "course/all.html", context)
	except KeyError:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})



def login_view(request):
	form = UserLoginForm(request.POST or None)
	title = "Login"
	context = {"form":form ,"title":title}
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

def edit_view(userkey,pk):
	previous_data = {"review":"","rating":0}
	edit = False
	try: #is it requested to edit
		user =  User.objects.filter(id = userkey)[0]
		course = CourseModel.objects.filter(id = pk)[0]
		previous = {"review":"","rating":0}
		d = CoursereviewModel.objects.all().filter(user_id = user.id)
		for x in d:
			if str(x.course_id) == str(pk):
				edit = True
				previous_data["review"] = x.review
				previous_data["rating"] = x.rating
	except IndexError:
		edit = False
		pass
	return edit,previous_data

def check_login(userkey):
	try:
		if userkey:
			return True
	except KeyError:
		return False

def add_rating(userkey,keyword,rating,pk):
	data_list = CoursereviewModel()
	data_list.user =  User.objects.filter(id = userkey)[0]
	data_list.rating = int(rating)
	data_list.review = keyword
	data_list.course = CourseModel.objects.filter(id = pk)[0]
	data_list.save()

def update_rating(userkey,keyword,rating,pk):
	user =  User.objects.filter(id = userkey)[0]
	course = CourseModel.objects.filter(id = pk)[0]
	d = CoursereviewModel.objects.all().filter(user_id = user.id)
	for x in d:
		if str(x.course_id) == str(pk):
			x.review = keyword
			CoursereviewModel.objects.all().filter(user_id = user.id).filter(course_id = \
			pk).update(review = keyword,rating = int(rating))


def rating_view(request,pk):
	userkey,rating,edit = request.session['member_id'],request.POST.get("rating"),False
	edit,previous_data = edit_view(userkey,pk) #checks whether to edit or new form
	searchform = SearchForm(request.POST or None,initial = { 'previous_data':previous_data})
	if check_login(userkey): #checks whether the user is Logged in
		if searchform.is_valid():
			keyword = searchform.cleaned_data.get("keyword")
			if not edit:
				add_rating(userkey,keyword,rating,pk) #creates review and rating for the selected course
			else:
				update_rating(userkey,keyword,rating,pk) #updates review and rating for the selected course
			return HttpResponseRedirect('/all/')
		context = {"form":searchform,'previous_data':previous_data}
		return render(request, "course/rating.html", context)
	else:
		form = "Please login to proceed"
		return render(request,"course/index.html",{"form":form})

def pagination(page	):
	courses_list = CourseModel.objects.all()
	paginator = Paginator(courses_list, 10)
	try:
		courses_list_limited = paginator.page(page)
	except PageNotAnInteger:
		courses_list_limited = paginator.page(1)
	except EmptyPage:
		courses_list_limited = paginator.page(paginator.num_pages)
	return courses_list_limited

def allcourse_view(request):
	try:
		if request.session['member_id']:
			page = request.GET.get('page')
			context = {"list1":pagination(page),"title":"Courses"}
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

def register_view(request):
	form = UserRegisterForm(request.POST or None)
	title = "Register"
	if form.is_valid():
		user = form.save(commit = False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		login(request,user)
		return HttpResponseRedirect('/all/')
	context = {"form":form ,"title":title}
	return render(request,"course/form.html",context)

def logout_view(request):
	print logout(request)
	try:
		del request.session['member_id']
	except KeyError:
		pass
	form = "Logged out successfully"
	return render(request,"/login/",{"form":form})
