document.addEventListener('DOMContentLoaded', function() {

	// If add review exists then we're on the recipe page
	if(document.querySelector("#add-review-button")){
		document.querySelector("#add-review").style.display = "none";
		document.querySelector("#view-reviews").style.display = "none";
		document.querySelector("#add-to-list").style.display = "none";
		document.querySelector("#view-reviews-button").addEventListener("click",viewReviews);
		document.querySelector("#add-to-list-button").addEventListener("click",addToList);
		document.querySelector("#add-review-button").addEventListener("click",addReview);

		let closeButtons = document.querySelectorAll(".close-bar .close-modal");

		// Adds close modal functions to modal
		for (let i = 0; i < closeButtons.length; i++) {
		    closeButtons[i].addEventListener("click", closeModal);
		}
		
	}else if(document.querySelector("#view-reviews-button")){
		document.querySelector("#add-review").style.display = "none";
		document.querySelector("#view-reviews").style.display = "none";
		document.querySelector("#add-to-list").style.display = "none";
		document.querySelector("#view-reviews-button").addEventListener("click",viewReviews);
		// Close modal buttons
		let closeButtons = document.querySelectorAll(".close-bar .close-modal");

		// Adds close modal functions to modal
		for (let i = 0; i < closeButtons.length; i++) {
		    closeButtons[i].addEventListener("click", closeModal);
		}
	}


	// Edit Recipe Form
	if(document.querySelector("#delete-recipe")){
		// Open and close delete recipe modal
		document.querySelector("#delete-recipe").style.display = "none";
		document.querySelector("#delete-recipe-button").addEventListener("click",deleteRecipe);
		document.querySelector("#delete-recipe .close-bar .close-modal").addEventListener("click", closeModal);
	}

	// Delete Review
	if(document.querySelector("#delete-review")){
		// Open and close delete review modal
		document.querySelector("#delete-review").style.display = "none";
		for(let i = 0; i < document.querySelectorAll(".delete-review-button").length; i++){
			document.querySelectorAll(".delete-review-button")[i].addEventListener("click",deleteReview);
		}
		document.querySelector("#delete-review .close-bar .close-modal").addEventListener("click", closeModal);
	}

	// Delete Comment
	if(document.querySelector("#delete-comment")){
		// Open and close delete comment modal
		document.querySelector("#delete-comment").style.display = "none";
		for(let i = 0; i < document.querySelectorAll(".delete-comment-button").length; i++){
			document.querySelectorAll(".delete-comment-button")[i].addEventListener("click",deleteComment);
		}
		document.querySelector("#delete-comment .close-bar .close-modal").addEventListener("click", closeModal);
	}

	document.querySelector("#edit-recipe-list .close-bar .close-modal").addEventListener("click", closeModal);

	// Edit Recipe List
	document.querySelector("#save-recipe-list").addEventListener("click", saveRecipeList);

	// Captures all edit buttons on page
	let editButtons = document.querySelectorAll(".edit-list-button");
	
	// Adds editRecipeList function to all available edit buttons on page
	for (let i = 0; i < editButtons.length; i++) {
	    editButtons[i].addEventListener("click", editRecipeList);
	}


});

// Get csrftoken, code is from this documentation https://docs.djangoproject.com/en/3.0/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Open add review modal, add checkstar function to all stars in rating panel
function addReview(){
	document.querySelector("#add-review").style.display = "block";

	let starButtons = document.querySelectorAll(".star-container input");
	for (let i = 0; i < starButtons.length; i++) {
	    starButtons[i].addEventListener("click", checkStar);
	}
}

// Highlights all stars before clicked star
function checkStar(){
	for(let i = 1; i <= 5; i++){
		document.querySelector("#star" + i + " ~" + " .checkmark").style.background = "grey";
	}
	starLength = event.target.value;
	document.querySelector("#star" + event.target.value + " ~" + ".checkmark").style.background = "gold";
	for(let k = 1; k < starLength; k++){
		document.querySelector("#star" + k + " ~" + " .checkmark").style.background = "gold";
	}
}

// Opens View Reviews Modal
function viewReviews(){
	document.querySelector("#view-reviews").style.display = "block";
}

// Opens add to Recipe List moda,
function addToList(){
	document.querySelector("#add-to-list").style.display = "block";	
}

// Attach it to every Close button and closes modal
function closeModal(){
	this.parentNode.parentNode.style.display = "none";
}

function editRecipeList(){
	document.querySelector("#edit-recipe-list").style.display = "block";

	let recipeListId = this.getAttribute("data-list-id");
	document.querySelector("#save-recipe-list").setAttribute("data-list-id", recipeListId);

	let recipeListName = document.querySelector("#recipe-list-name");
	let publicStatus = document.querySelector("#list-public-status");

	fetch('/editlist/' + recipeListId + '/status')
	.then(response => response.json())
	.then(status=> {
		recipeListName.value = status.name;
		publicStatus.checked = status.status;
	});


	document.querySelector("#delete-recipe-list").addEventListener("click", function(){ deleteRecipeList(recipeListId); });
}

async function saveRecipeList(){
	// Gets new content and creates token
	let recipeListId = this.getAttribute("data-list-id");
	let listContainer = document.querySelector('button[data-list-id="'+recipeListId+'"]').parentNode;
	let listContainerTitle = listContainer.querySelector('.card-title a');
	let token = getCookie('csrftoken');
	// Saves info from edit textbox to recipe
	let recipeListName = document.querySelector("#recipe-list-name").value;
	let publicStatus = document.querySelector("#list-public-status").checked;

	await fetch('/editlist/' + recipeListId, {
		  headers: {
			'X-CSRFToken': token
		  },
          method: 'PUT',
          body: JSON.stringify({
                name: recipeListName,
                public: publicStatus
          })
    });

	listContainerTitle.innerHTML = recipeListName;
    document.querySelector("#edit-recipe-list").style.display = "none";
}

// Opens Delete Recipe Modal
function deleteRecipe(){
	document.querySelector("#delete-recipe").style.display = "block";
}

// Opens Delete Recipe List Modal
function deleteRecipeList(recipeListId){
	document.querySelector("#delete-recipe-list-modal").style.display = "block";		  
	document.querySelector("#confirm-delete-recipe-list").setAttribute("href", "/deletelist/" + recipeListId);
}

// Opens Delete Review Modal
function deleteReview(){
	document.querySelector("#delete-review").style.display = "block";
	let reviewId = this.getAttribute("data-review-id");
	document.querySelector("#confirm-delete-review").setAttribute("href", "/deletereview/" + reviewId);
}

// Opens Delete Review Modal
function deleteComment(){
	document.querySelector("#delete-comment").style.display = "block";
	let commentId = this.getAttribute("data-comment-id");
	document.querySelector("#confirm-delete-comment").setAttribute("href", "/deletecomment/" + commentId);
}