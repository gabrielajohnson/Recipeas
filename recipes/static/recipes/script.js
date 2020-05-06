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
	// Prevents the edit post button from opening multiple forms 
	// By checking if the post content is already hidden
	if(this.parentNode.querySelector("h5").style.display != "none"){

		// Creates Edit Form
		let editForm = document.createElement("form");

		// Creates textbox for edit
		let editTextbox = document.createElement("input");
		editTextbox.classList.add("d-block","mb-1","w-100");
		editTextbox.type = "text";
		editTextbox.value = this.parentNode.querySelector("h5").innerText;
		let recipeListId = this.getAttribute("data-id");

		//Create checkbox for public status
		let publicStatus = document.createElement("input");
		publicStatus.classList.add("d-block","mb-1","w-100");
		publicStatus.type = "checkbox";

		fetch('/editlist/' + recipeListId + '/status')
		.then(response => response.json())
		.then(status=> {
			console.log("hi" + status.status);
			if(status.status){
				publicStatus.checked = true;
			}
		});

		// Creates save changes button and adds function to save the edit
		let saveChanges = document.createElement("input");
		saveChanges.value = "Save Changes";
		saveChanges.type = "button";
		saveChanges.classList.add("btn","btn-outline-success","m-1");
		saveChanges.addEventListener("click",() => saveRecipeList(this.parentNode,editTextbox,recipeListId,publicStatus));
		
		// Creates cancel button so the user can cancel the changes and revert the post back to its prior state
		let cancel = document.createElement("button");
		cancel.innerHTML = "Cancel";
		cancel.addEventListener("click",() => cancelEdit(cancel,this.parentNode));
		cancel.classList.add("btn","btn-outline-danger","m-1");

		// All elements are appended to the form
		editForm.append(editTextbox);
		editForm.append(publicStatus);
		editForm.append(saveChanges);
		editForm.append(cancel);

		// Hides original post text and appends editForm for user to view
		this.parentNode.querySelector("h5").style.display = "none";
		this.parentNode.append(editForm);
	}
}

async function saveRecipeList(listContainer,editTextbox,recipeListId,publicStatus){
	// Gets new content and creates token
	let newContent = editTextbox.value;
	let status = publicStatus.checked;
	let token = getCookie('csrftoken');
	// Saves info from edit textbox to recipe
	await fetch('/editlist/' + recipeListId, {
		  headers: {
			'X-CSRFToken': token
		  },
          method: 'PUT',
          body: JSON.stringify({
                name: newContent,
                public: status
          })
    });
    // Removes textbox form after save
    editTextbox.parentNode.remove();
	listContainer.querySelector("h5").style.display = "block";
	listContainer.querySelector("h5 a").innerText = newContent;
}

function cancelEdit(cancel,listContainer){
	// Cancel edit, will remove editForm and display original post text
	cancel.parentNode.remove();
	listContainer.querySelector("h5").style.display = "block";
}