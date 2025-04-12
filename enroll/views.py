from django.shortcuts import render, redirect
from .forms import UserForm
from .mongodb import users_collection  # Import MongoDB connection
from django.core.files.storage import default_storage
from django.http import HttpResponse,JsonResponse
from django.core import serializers
import json
from bson import json_util
#  CREATE (Add User)
def add(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle image upload
            image_path = None
            if request.FILES.get('Profile_Images'):
                image = request.FILES['Profile_Images']
                image_path = default_storage.save(f"student_images/{image.name}", image)

            # Save user data in MongoDB
            user_data = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
                "Profile_Images": image_path  # Store the image path
            }
            # Correct print statements
            print(user_data['name'])  
            print(user_data['password'])
            users_collection.insert_one(user_data)  # Save to MongoDB
            print("Form submitted successfully")
            return redirect('show')
        else:
            print("Error:", form.errors)

    else:
        form = UserForm()
    return render(request, 'enroll/add.html', {"forms": form})


# READ (Show Users)
def show(request):
    students = list(users_collection.find())  # Convert cursor to list
    students_json = json_util.dumps(students)  # Serialize with bson's json_util
    return HttpResponse(students_json, content_type="application/json")
# render(request, 'enroll/show.html', {"student": students})

# UPDATE (Edit User)
def update(request, email):
    user = users_collection.find_one({"email": email})

    if not user:
        return redirect('show')

    if request.method == "POST":
        form_edit = UserForm(request.POST, request.FILES)
        if form_edit.is_valid():
            updated_data = {
                "name": form_edit.cleaned_data["name"],
                "email": form_edit.cleaned_data["email"],
                "password": form_edit.cleaned_data["password"],
            }

            # Handle profile image update
            if request.FILES.get("Profile_Images"):
                image = request.FILES["Profile_Images"]
                image_path = default_storage.save(f"student_images/{image.name}", image)
                updated_data["Profile_Images"] = image_path  # Update image path in MongoDB
            else:
                updated_data["Profile_Images"] = user.get("Profile_Images")  # Retain old image if not updated

            users_collection.update_one({"email": email}, {"$set": updated_data})
            return redirect('show')
    else:
        form_edit = UserForm(initial={
            "name": user["name"],
            "email": user["email"],
            "password": user["password"],
        })

    return render(request, 'enroll/update.html', {'form_edit': form_edit})


#  DELETE (Remove User)
def delete(request, email):
    if request.method == 'POST':
        users_collection.delete_one({"email": email})
    return redirect('show')

#  ADMIN View (Show Users Without `_id`)
def admin_users(request):
    students = list(users_collection.find({}, {"_id": 0}))  
    return render(request, 'enroll/admin_users.html', {"students": students})
