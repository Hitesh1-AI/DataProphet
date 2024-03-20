function uploadFile() {
    const fileInput = document.getElementById("csvFile");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("csv_file", file);

    fetch("/uploaded", {
        method: "POST",
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        // Handle the response from the backend
        // console.log(data);
        window.location.href= '/index.html';
    })
    .catch((error) => {
        // Handle any errors
        console.error("Error:", error);
    });
}

console.log("enter in script");
document.addEventListener("DOMContentLoaded", function() {
    console.log("Script loaded and DOM is ready");
    document.getElementById("csvForm").addEventListener("submit", uploadFile);
});

