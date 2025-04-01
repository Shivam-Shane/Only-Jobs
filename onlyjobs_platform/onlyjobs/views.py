import os,sys
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

# Adding the project root directory to the PYTHONPATH for imports from upper level
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_path)
from datetime import datetime
from user_signup import Usercreation
from login_verify import verify_login
from user_details import get_user_details,update_user_details
from posts import post_fetcher,post_creater
from profile_picture import update_profile_picture
from llm_process import PostAuthenticityChecker
from logger import logging
from forget_password import Password_reset
from gmail_connector import MailSender
from django.conf import settings

# ----------------------------------------------------------------
user_creation_object=Usercreation()
password_reset_object=Password_reset()
mail_sender_object=MailSender()
postauthchecker=PostAuthenticityChecker()
# ----------------------------------------------------------------


wrong_otp=0  # global variable
def home(request):

    if request.session.get('user_email'):
            user_detail,posts=user_detail_post(request)
            if user_detail:
                context={
                    'user_detail': user_detail,
                    'time': datetime.now(),
                    'posts': posts,
                    'MEDIA_URL': settings.MEDIA_URL  # for dynamic media urls 
                }
                return render(request, 'home.html',context)
            # else return only post data with default value for all user feilds
            # return render(request, 'home.html',context={  'posts': posts  })  # Serve actual home content if authenticated
    # If not authenticated it will return to login page for login purposes
    return render(request, 'login.html')

def user_detail_post(request):
    user_detail=_helper_user_details(request)
    posts = post_details(request)
    return user_detail,posts

def _helper_user_details(request):
    # This function is used to retrieve user details from the session or database
    user_email = request.session.get('user_email')
    default_data = {
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'address': 'Not Provided',
    'profile_pic': 'defaultprofilepic.png',
    'birth_date': '01-01-2000',
    'designation': 'User',
    'company': 'Only Jobs',
    'workstartdate': 'Not Provided',
    'workenddate': 'Not Provided',
    'qualification': 'Not Provided'
}
    
    if user_email:
        user_data=get_user_details(user_email)    
        
        for key, default_value in default_data.items():
            if user_data.get(key) is None:  # Check if the value is None
                user_data[key] = default_value
        return user_data    
    else:
        return None

def login_view(request):
    if request.session.get('user_email'):
        # If session exists, redirect to home page or dashboard
        logging.info("Session exists, redirecting to home page")
        return redirect('home')

    if request.method == 'POST':
        useremail = request.POST.get('useremail')
        password = request.POST.get('password')
        status,user_id=verify_login(useremail,password)
        if status:
            try:
                user = {
                    'user_id':user_id,
                    'user_email': useremail,  # user_email/user_id is stored now in session
                }
                # Manually create a session variable for the authenticated user
                request.session['user_email'] = user['user_email']
                request.session['user_id']=user['user_id']

                logging.info(f'User {useremail} logged in successfully')
                messages.success(request,f"User {useremail} logged in successfully")
                return redirect('home')
            except Exception as e:
                    logging.error(f'Error while fetching user: {e}')
                    messages.error(request, 'An error occurred while logging you in.')
        else:
            messages.error(request, 'Invalid username/password or user does not exist')

    return render(request, 'login.html')

def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone')
        password = request.POST.get('password')
        
        try:
            logging.info(f'Signing UP user: %s', username)
            
            return_value = user_creation_object.user_availbilty(username, phone_no)
            if return_value == 'UserAccount available':
                send_otp = mail_sender_object.signup_otp_sending(email)
                if send_otp:
                    
                    # Store the otp, username, name, password, and email in session
                    user_details={
                        'otp': send_otp,
                        'username': username,
                        'name': name,
                        'password': password,
                        'email': email,
                        'phone_no': phone_no,
                    }
                    # Manually create a session for the user with details
                    request.session['sent_otp'] = user_details['otp']
                    request.session['username'] = user_details['username']
                    request.session['name'] = user_details['name']
                    request.session['phone_no'] = user_details['phone_no']
                    request.session['email'] = user_details['email']
                    request.session['password'] = user_details['password']
                    

                    # Return success response
                    return JsonResponse({
                        'status': 'success',
                        'message': 'A OTP has been sent to your email address'
                    })
            elif return_value in ['Phone No And Username Already Exists',
                                        'Phone No Already Exists',
                                        'Username already Exists'
                                            ]:
                return JsonResponse({   #Return failure response
                    'status': 'error',
                    'message': return_value
                })
            
            else:
                logging.error(f'Error creating user: {username}')
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error creating user. Please try again later.'
                })
        except Exception as e:
            logging.error(f'Error creating user {username}, exception occurred: {e}')
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred. Please contact support.'
            }, status=500)  # HTTP 500 for server error

    # For non-POST requests, render the default page
    return render(request, 'login.html')

def verify_otp(request):
    global wrong_otp
    if request.method=='POST':
        sentotp=request.session.get('sent_otp') # Stored otp in session
        user_otp=request.POST.get('otp') # Otp entered by user

        if user_otp==sentotp and wrong_otp<5:
            username=request.session.get('username')
            name=request.session.get('name')
            phone_no=request.session.get('phone_no')
            email=request.session.get('email')
            password=request.session.get('password')
            
            result=user_creation_object.create_user(username,name,phone_no,email,password)
            if result:
                messages.success(request, "User created successfully! You can now log in.")
                request.session.clear() # clear session data
                return JsonResponse({
                        'status': 'success',
                        'redirect_url': reverse('login')
                    })
            else:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'An error occurred while creating the user',
                    'redirect_url': reverse('login')
                })
        elif wrong_otp>=5:
            return JsonResponse({
                        'status': 'Failed',
                        'message': 'Too many wrong attempts. Please try again after some time.',
                        'redirect_url': reverse('login')
                    })
        else: 
            wrong_otp+=1
            return JsonResponse({
                        'status': 'Failed',
                        'message': 'Invalid OTP'
                    })

def logout(request):
    
    if request.session.get('user_email'):# Clear the session and redirect to login page
        request.session.clear()
        logging.debug("User logged out successfully")
        # Clear existing messages
        storage = messages.get_messages(request)
        for _ in storage:  # Consume and clear messages
            pass
        messages.success(request, "You have been logged out successfully")
        return redirect('login')
    else:
        messages.error(request, "No session available for logging out")
        return redirect('login')

def forget_password(request):
    if request.method=='POST':
        useremail=request.POST.get('useremail')
        # Call the reset_password function once and store the result
        password_reset_result = password_reset_object.reset_password(useremail)
        
        # Create a message based on the result
        if password_reset_result:
            message = "A new password has been sent to your email address."
            messages.success(request, message)
        else:
            message = "Your email address is not assosicated with us. Please check and try again."
            messages.error(request, message)

    return render(request, 'forget_password.html')

def post_details(request):
    fetched_posts=post_fetcher()
    return fetched_posts 

def post_create(request):
    if request.method == 'POST':

        user_id=request.session.get('user_id')
        post_content=request.POST.get('postContent')
        
        # Call the post_create function once and store the result
        if len(post_content)>20:
            postfile=None
            directory=settings.MEDIA_ROOT
            if 'postfile' in request.FILES:
                postfile = request.FILES['postfile']
            post_validator=postauthchecker.check_post_authenticity(post_content)  
            if post_validator=='valid':
                post_creation_result = post_creater(user_id,post_content,postfile,directory[0])
                # Create a message based on the result
                if post_creation_result:
                    message = "Your post has been created successfully."
                    messages.success(request, message)
                else:
                    message = "An error occurred while creating your post. Please try again."
                    messages.error(request, message)
                return redirect('home')
            elif post_validator=='invalid':
                message = "Oops! This post doesn't seem to be a valid job listing. Please check and try again."
                messages.error(request, message)
                return redirect('home')
            
        else: 
            message = "Post content should be at least 20 characters long."
            messages.error(request, message)
    return redirect('home')

def jobs_listing(request):
    user_detail,_=user_detail_post(request)
    context={
                    'user_detail': user_detail,
                    'time': datetime.now(),
                    'MEDIA_URL': settings.MEDIA_URL  # for dynamic media urls 
                }
    return render(request, 'jobs.html',context)

def notification(request):
    return redirect('home')

def profile_update(request):
    
    # If the method is POST, handle the form submission
    if request.method == 'POST':
        # Get the session data
        user_email = request.session.get('user_email')
        user_id = request.session.get('user_id')

        # Check if user is logged in (if session doesn't have user info, redirect to login)
        if not user_email or not user_id:
            messages.error(request, 'User not authenticated.')
            return redirect('login')  # Redirect to the login page

        # Get the form data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        qualification = request.POST.get('qualification')
        designation = request.POST.get('designation')
        company = request.POST.get('company')

        # Prepare the user details for updating
        user_details = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'qualification': qualification,
            'designation': designation,
            'company': company,
            'user_email': user_email,
        }

        # Assuming update_user_details() updates the database with the new details
        if update_user_details(user_details):
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_update')  # Redirect to profile page after success
        
        # If update failed, show an error message
        messages.error(request, 'Failed to update profile. Please try again.')
        return redirect('profile_update')  # Redirect to profile page on failure

    # If the method is GET, render the profile page with user details
    else:
        # Retrieve session data
        user_email = request.session.get('user_email')
        user_id = request.session.get('user_id')

        # Check if the user is logged in (redirect to login if not)
        if not user_email or not user_id:
            return redirect('login')  # Redirect to the login page if user is not authenticated

        # Fetch user details, assuming _helper_user_details() gets the user's profile info
        user_detail = _helper_user_details(request)
        
        # Ensure there is always an HttpResponse object returned, even if no user detail found
        if user_detail:
            context = {'user_detail': user_detail, 
                       'user_email': user_email,
                       'time': datetime.now(),
                       'MEDIA_URL': settings.MEDIA_URL  # for dynamic media urls
                       }
        else:
            context = {'user_email': user_email,
                       'time': datetime.now(),
                       'MEDIA_URL': settings.MEDIA_URL  # for dynamic media urls
                       }

        return render(request, 'profile.html', context)  # Return the profile page with context

def profile_picture_upload(request):
    # If the method is POST, handle the form submission
    if request.method == 'POST':
        logging.info("Starting profile picture upload")
        
        # Get the session data
        user_id = request.session.get('user_id')
        
        if 'newProfilePicture' in request.FILES:
            profile_image = request.FILES['newProfilePicture']

            filepath=settings.MEDIA_ROOT
            status=update_profile_picture(user_id,profile_image,filepath[0])
            if status:
                logging.info("Profile picture uploaded successfully:")
                messages.success(request, 'Profile picture updated successfully.')
                return redirect('profile_update')
            
            # Show success message and redirect
            
        else:
            # Handle missing file error
            logging.error("No profile picture found in the request.")
            messages.error(request, 'Failed to update profile picture. Please try again.')
            return redirect('profile_update')

    return redirect('profile_update')

def custom_404_view(request,exception):
    return render(request, '404.html', status=404)