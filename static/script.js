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

  if (addGoodHabitButton) {
    addGoodHabitButton.addEventListener("click", () => {
      const habit_name = prompt("Enter habit name");
      if (!habit_name) return;

      fetch("/addGoodHabit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ habit_name })
      })
      .then(res => res.json())
      .then(data => {
        console.log(data.habit_name);
      })
      .catch(err => console.error(err));
    });
  }

  const addBadHabitButton = document.getElementById("addGoodHabit");

  if (addBadHabitButton) {
    addBadHabitButton.addEventListener("click", () => {
      const habit_name = prompt("Enter habit name");
      if (!habit_name) return;

      fetch("/addBadHabit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ habit_name })
      })
      .then(res => res.json())
      .then(data => {
        console.log(data.habit_name);
      })
      .catch(err => console.error(err));
    });
  }
});