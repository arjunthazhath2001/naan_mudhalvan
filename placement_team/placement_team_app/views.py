from django.contrib import messages 
# Import Django's 'messages' framework, which is used to display one-time notifications like success or error messages to the user.

from django.shortcuts import render, redirect
# Import 'render' for rendering templates (HTML pages) and 'redirect' to redirect the user to another page after certain actions.

from django.contrib.auth import authenticate, login
# Import Django's built-in authentication methods. 'authenticate' verifies the user’s credentials, and 'login' logs in the authenticated user.

from django.contrib.auth.decorators import login_required
# Import 'login_required', a decorator that ensures certain views can only be accessed by logged-in users. If a user isn't logged in, they will be redirected to the login page.

from .models import Job_fairs
# Import the 'Job_fairs' model from the current app’s models file. This is where data about job fairs (like district, date, etc.) is stored in the database.

import qrcode
# Import the 'qrcode' library, which allows generating QR codes.

from io import BytesIO
# Import 'BytesIO', which allows in-memory file operations (like saving an image in memory before saving it to the database).

from django.core.files.base import ContentFile
# Import 'ContentFile', which allows saving in-memory files (like a QR code image) into Django model fields.

# Create your views here.
# This is a placeholder comment often included in Django views files, indicating where the view functions are defined.

def login_view(request):
    # Define a view function called 'login_view', which handles user login. The 'request' object contains all the data about the current request.
    
    if request.method == "POST":
        # Check if the HTTP request method is POST, which means the form was submitted (login data was sent).
        
        username = request.POST.get('username')
        # Get the 'username' from the submitted POST data.

        password = request.POST.get('password')
        # Get the 'password' from the submitted POST data.
        
        user = authenticate(request, username=username, password=password)
        # Authenticate the user using the provided username and password. If credentials are valid, 'user' will be an object, otherwise None.
        
        if user is not None:
            # If authentication was successful (user is not None),
            
            login(request, user)
            # Log the user in using Django's 'login' function.
            
            return redirect('index')
            # Redirect the user to the 'index' page (home page) after a successful login.
        
        else:
            # If authentication fails (user is None),
            
            messages.error(request, "Invalid username or password")
            # Display an error message using Django's 'messages' framework.
    
    return render(request, 'placement_team_app/login.html')
    # If the request method is not POST (i.e., the user is visiting the login page), render the login page template ('login.html').

# Index view with login protection
@login_required(login_url='login')
# The 'index' view requires the user to be logged in. If they are not, they will be redirected to the 'login' page.

def index(request):
    # Define the 'index' view, which will display the home page for the logged-in users.
    
    success_message = ""
    # Initialize an empty 'success_message' variable to store a success notification after an operation (like creating a job fair).
    
    qr_image = None
    # Initialize 'qr_image' to None. This will later hold the URL of the generated QR code image.
    
    if request.method == "POST":
        # If the request method is POST (indicating a form submission),
        
        district = request.POST.get('district')
        # Get the 'district' input from the POST data.
        
        date_of_job_fair = request.POST.get('job-fair-date')
        # Get the 'date_of_job_fair' input from the POST data.
        
        job_fair = Job_fairs(district=district, date_of_job_fair=date_of_job_fair)
        # Create a new instance of the 'Job_fairs' model with the submitted district and date_of_job_fair values.
        
        job_fair.save()
        # Save the newly created 'job_fair' object to the database.
        
        qr_code_image = generate_qr_code_image(job_fair.job_fair_id)
        # Call the 'generate_qr_code_image' function, passing the job fair's ID. This function returns the QR code image in binary format.
        
        job_fair.qr_code.save(f"qr_{job_fair.job_fair_id}.png", ContentFile(qr_code_image))
        # Save the QR code image to the 'qr_code' field of the 'job_fair' object, using the job fair ID in the file name.
        
        job_fair.save()
        # Save the 'job_fair' object again, now with the QR code attached.
        
        success_message = "Job fair created and QR generated"
        # Set the success message to indicate that the job fair was created and the QR code was generated.
        
        qr_image = job_fair.qr_code.url
        # Store the URL of the saved QR code image in 'qr_image'.
    
    return render(request, 'placement_team_app/index.html', {
        'success_message': success_message,
        'qr_image': qr_image
        # Render the 'index.html' template and pass the 'success_message' and 'qr_image' variables to the template.
    })

def generate_qr_code_image(job_fair_id):
    # Define a helper function to generate a QR code image for a given 'job_fair_id'.
    
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L, 
                       box_size=10, border=4)
    # Create a new QRCode object. 'version=1' sets the size of the QR code, 'ERROR_CORRECT_L' is the error correction level, 'box_size=10' defines the size of each box, and 'border=4' sets the width of the QR code border.
    
    registration_link = f"https://youtube.com"
    # Set a mock registration link (in practice, this would likely be a registration page for the job fair).
    
    qr.add_data(f"Job Fair ID: {job_fair_id}, Link: {registration_link}")
    # Add the job fair ID and the registration link as data in the QR code.
    
    qr.make(fit=True)
    # Generate the QR code with the provided data, ensuring that it fits properly.
    
    img = qr.make_image(fill="black", back_color='white')
    # Create the QR code image, specifying the fill color as black and the background as white.
    
    byte_io = BytesIO()
    # Create a BytesIO object, which allows the image to be saved in memory (as opposed to saving it to disk).
    
    img.save(byte_io, 'PNG')
    # Save the QR code image in PNG format to the BytesIO object.
    
    byte_io.seek(0)
    # Move the file pointer of the BytesIO object back to the start, so it can be read from the beginning.
    
    return byte_io.getvalue()
    # Return the binary content (the image data) of the QR code, which will later be saved to the database.
