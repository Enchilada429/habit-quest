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
      fetch("/test/4", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ count: 5 })
      })
      .then(res => res.json())
      .then(data => {
        console.log(data.newCount);
      });
      console.log("CTA button clicked");
      alert("Welcome! This is your starting point.");
    });
  }

  const addGoodHabitButton = document.getElementById("addGoodHabit");

  if (addGoodHabitButton) {
    addGoodHabitButton.addEventListener("click", function () {
      
    });
  }
});
