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
    const editButton = document.getElementById("editButton");
    const editModal = document.getElementById("editModal");
    const closeModal = document.getElementById("closeModal");
    const cancelButton = document.getElementById("cancelButton");
    
    // Open the modal when Edit button is clicked
    editButton.addEventListener("click", () => {
        editModal.style.display = "block";
    });
    
    // Close the modal when the close button or cancel button is clicked
    closeModal.addEventListener("click", () => {
        editModal.style.display = "none";
    });

    cancelButton.addEventListener("click", () => {
        editModal.style.display = "none";
    });

    // Optional: Close the modal when clicking outside the modal content
    window.addEventListener("click", (e) => {
        if (e.target === editModal) {
            editModal.style.display = "none";
        }
    });
});
