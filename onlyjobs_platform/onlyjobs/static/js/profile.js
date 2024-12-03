let profileMenu = document.getElementById("profileMenu");

function toggleMenu(){
    profileMenu.classList.toggle("open-menu");
}

let sideActivity = document.getElementById("sidebarActivity");
let moreLink = document.getElementById("showMoreLink");

function toggleActivity(){
    sideActivity.classList.toggle("open-activity");
    if (sideActivity.classList.contains("open-activity")) {
        moreLink.innerHTML="Show less <b>-</b>";
        
    }
    else{
        moreLink.innerHTML="Show More <b>+</b>";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const edituserButton = document.getElementById("edituserButton");
    const edituserModal = document.getElementById("edituserModal");
    const usercloseModal = document.getElementById("usercloseModal");
    const usercancelButton = document.getElementById("usercancelButton");
    
    // Open the modal when Edit button is clicked
    edituserButton.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent form submission or other default actions
        edituserModal.classList.add("open"); // Show modal by adding a class
    });
    
    // Close the modal when the close button or cancel button is clicked
    usercloseModal.addEventListener("click", () => {
        edituserModal.classList.remove("open"); // Hide modal by removing the class
    });

    usercancelButton.addEventListener("click", () => {
        edituserModal.classList.remove("open"); // Hide modal on cancel
    });

    // Optional: Close the modal when clicking outside the modal content
    window.addEventListener("click", (e) => {
        if (e.target === edituserModal) {
            edituserModal.classList.remove("open");
        }
    });
});

// Get image upload modal and close button elements
var uploadModal = document.getElementById("uploadModal");
var closeModaluploadimage = document.getElementById("closeModaluploadimage");

// Open the modal when the profile picture is clicked
document.getElementById("profilePicWrapper").addEventListener("click", function() {
    uploadModal.style.display = "block"; // Show the modal
});

// Close the modal when the 'x' is clicked
closeModaluploadimage.addEventListener("click", function() {
    uploadModal.style.display = "none"; // Hide the modal
});

// Close the modal if the user clicks anywhere outside the modal content
window.addEventListener("click", function(event) {
    if (event.target == uploadModal) {
        uploadModal.style.display = "none";
    }
});

// Preview selected image before upload 
function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('.profile-pic');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}
