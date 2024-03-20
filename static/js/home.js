
function UpNext() {

    fetch("/home", {
        method: "GET"
    })
    .then((response) => response.text())
    .then((data) => {
        // Handle the response from the backend
        // console.log(data);
        document.getElementById("m").innerHTML = data;
        history.pushState({}, "", "/home");
    })
    .catch((error) => {
        // Handle any errors
        console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("home").addEventListener("click", UpNext);
});
