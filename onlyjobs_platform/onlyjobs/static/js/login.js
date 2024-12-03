// Show password toggle logic for login and signup forms (no changes here)
const passwordInput_login = document.getElementById('password-login');
const togglePassword_login = document.getElementById('togglePassword-login');
togglePassword_login.addEventListener('click', () => {
  const type = passwordInput_login.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordInput_login.setAttribute('type', type);
  togglePassword_login.textContent = type === 'password' ? '👁️' : '🙈';
});

const togglePasswordSignup = document.getElementById('togglePassword-signup');
const passwordSignup = document.getElementById('password-signup');
togglePasswordSignup.addEventListener('click', function () {
  const type = passwordSignup.type === 'password' ? 'text' : 'password';
  passwordSignup.type = type;
  this.textContent = type === 'password' ? '👁️' : '🙈';
});

// Handle signup form submission
document.getElementById('submitBtn').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent default form submission
  const form = document.getElementById('signupForm');  // Access the form directly by ID
  const formData = new FormData(form);  // Create FormData from the form element
  
  // Show loading state or indication that the form is submitting
  document.getElementById('submitBtn').disabled = true;  // Disable the submit button to avoid multiple clicks
  document.getElementById('submitBtn').value = 'Submitting...'; // Change button text

  // Add CSRF token to fetch headers
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch(form.getAttribute('action'), {  // Use form's action attribute for the fetch URL
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrfToken  // Include CSRF token in the request headers
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response
  })
  .then(data => {
    console.log("Response data:", data); // Log the data returned by the backend

    if (data.status === 'success') {
      // Show the OTP popup only on success
      document.getElementById('otpPopup').style.display = 'block';
    } else {
      // Show error message from the backend if it's not a success
      alert(data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  })
  .finally(() => {
    // Re-enable the submit button after request completes
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').value = 'Submit'; // Reset button text
  });
});


// Handle OTP validation submission
document.getElementById('validateBtn').addEventListener('click', function(event) {
  event.preventDefault();  // Prevent form submission

  const otp = document.getElementById('otp').value;  // Get OTP input value
  const formData = new FormData();  // Prepare the data to send
  formData.append('otp', otp);  // Append OTP to form data
  formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);  // CSRF token

  // Find the form element with action for 'verify_otp' URL
  const form = document.getElementById('otpForm');  // Ensure OTP form has an ID attribute like `otpForm`
  
  // Send OTP to the backend to verify
  fetch(form.getAttribute('action'), {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (response.redirected) {
          // If redirected, navigate to the new URL
          window.location.href = response.url;
          return null;  // Prevent further processing
      }
      return response.json();  // Parse JSON if no redirection
  })
  .then(data => {
    if (data.status === 'success') {
        // alert(data.message);  // Show success message
        document.getElementById('otpPopup').style.display = 'none';  // Hide popup
        window.location.href = data.redirect_url;  // Redirect to the provided URL
    } else {
        alert(data.message);  // Show error message
    }
})
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred, please try again.');
  });
});


