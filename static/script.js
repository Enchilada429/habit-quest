// Custom JavaScript: This is where you add interactivity to your website

// This event listener waits for the entire HTML page to load before running any code
document.addEventListener("DOMContentLoaded", function () {
  console.log("Page loaded!");

  // We find the button using its unique ID from the HTML
  const ctaButton = document.getElementById("cta-button");

  // Check if the button exists on the page before adding an event listener
  if (ctaButton) {
    // This function runs whenever the button is clicked
    ctaButton.addEventListener("click", function () {
      console.log("CTA button clicked");
      alert("Welcome! This is your starting point.");
    });
  }

  const addGoodHabitButton = document.getElementById("addGoodHabit");
  const modal = document.getElementById("modal");
  const saveModalButton = document.getElementById("saveModal")
  const closeModalButton = document.getElementById("closeModal");

  if (addGoodHabitButton) {
    addGoodHabitButton.addEventListener("click", function () {
      console.log("add good habit button clicked")
      modal.classList.add("open");
    });
  }

  if (saveModalButton) {
    // TODO: Needs to add to habits table
    closeModalButton.addEventListener("click", function () {
      modal.classList.remove("open")
    })
  }

  if (closeModalButton) {
    closeModalButton.addEventListener("click", function () {
      modal.classList.remove("open");
    })
  }

});
