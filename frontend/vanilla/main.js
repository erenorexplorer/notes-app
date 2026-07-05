let currentView = "home-view";

function showView(viewName) {
    // hide all views
    const allViews = document.querySelectorAll(".view");
    allViews.forEach((view) => {
        view.classList.add("hidden");
    });
    // show specified view
    const targetView = document.getElementById(viewName);

    if (!targetView) {
        console.error("Unknown view:", viewName);
        return;
    }

    targetView.classList.remove("hidden");
    currentView = viewName;
}

const newNoteButton = document.getElementById("new-note-button");
newNoteButton.addEventListener("click", () => {
    showView("new-note-view");
});

const cancelNewNoteButton = document.getElementById("cancel-new-note-button");
cancelNewNoteButton.addEventListener("click", () => {
    showView("home-view");
});

const newNoteForm = document.getElementById("new-note-form");
newNoteForm.addEventListener("submit", (event) => {
    event.preventDefault();
});

showView(currentView);