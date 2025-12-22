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
  const goodHabitModal = document.getElementById("goodHabitModal");
  const saveGoodModalButton = document.getElementById("saveGoodModal")
  const closeGoodModalButton = document.getElementById("closeGoodModal");

  if (addGoodHabitButton) {
    addGoodHabitButton.addEventListener("click", function () {
      console.log("add good habit button clicked")
      goodHabitModal.classList.add("open");
    });
  }

  if (saveModalButton) {
    // TODO: Needs to add to habits table
    saveGoodModalButton.addEventListener("click", function () {
      goodHabitModal.classList.remove("open")
    })
  }

  if (closeModalButton) {
    closeGoodModalButton.addEventListener("click", function () {
      goodHabitModal.classList.remove("open");
    })
  }

  const addBadHabitButton = document.getElementById("addBadHabit");
  const badHabitModal = document.getElementById("badHabitModal");
  const saveBadModalButton = document.getElementById("")

  if (addBadHabitButton) {
    addBadHabitButton.addEventListener("click", function () {
      badHabitModal.classList.add("open")
    })
  }

});
