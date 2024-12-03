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

// Show the modal when "Post" or "Write Something" is clicked
document.querySelectorAll("#openPostModal").forEach(button => {
button.addEventListener("click", function () {
    const modal = document.getElementById("postModal");
    modal.style.display = "block";
    modal.classList.add("show");
});
});

// Close the post modal when clicking "Cancel" or close button
document.querySelectorAll(" .btn-secondary").forEach(button => {
button.addEventListener("click", function () {
    const modal = document.getElementById("postModal");
    modal.style.display = "none";
    modal.classList.remove("show");
});
});

