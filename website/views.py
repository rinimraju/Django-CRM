from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from . forms import SignUpForm, AddRecord
from . models import Record


def home(request):
	records = Record.objects.all()
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			messages.success(request, 'You have been logged in successfully')
			return redirect('home')
		else:
			messages.success(request, 'There was an error in logging in.Please try again')
			return redirect('home')
	else:
		return render(request, 'home.html', {'records': records})

def logout_user(request):
	logout(request)
	messages.success(request, 'You have been logged out....')
	return redirect('home')
 
def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			#Authentication and Login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request,user)
			messages.success(request,'You have successfully logged in!')
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form': form})

	return render(request, 'register.html', {'form': form})

def customer_record(request,pk):
	if request.user.is_authenticated:
		customer_record = Record.objects.get(id=pk)
		return render(request,'record.html',{'customer_record': customer_record})
	else:
		messages.success(request, 'You have to be logged in to view the records...')
		return redirect('home')

def delete_record(request,pk):
	if request.user.is_authenticated:
		delete_record = Record.objects.get(id=pk)
		delete_record.delete()
		messages.success(request,"Record has been deleted successfully...")
		return redirect('home')
	else:
		messages.success(request,"You have to be logged in to delete the records...")
		return redirect('home')

def add_record(request):
	form = AddRecord(request.POST or None)
	if request.user.is_authenticated:
		if request.method == 'POST':
			if form.is_valid():
				form.save()
				messages.success(request,'Record Added...')
				return redirect('home')
		return render(request,'add_record.html', {'form':form})
	else:
		messages.success(request,"You have to be logged in to add the records...")
		return redirect('home')

def update_record(request,pk):
	if request.user.is_authenticated:
		curr_record = Record.objects.get(id=pk)
		form = AddRecord(request.POST or None, instance=curr_record)
		if form.is_valid():
			form.save()
			messages.success(request,"Record has been updated successfully...")
			return redirect('home')
		return render(request,'update_record.html', {'form': form})
	else:
		messages.success(request,"You have to be logged in to update the records...")
		return redirect('home')
