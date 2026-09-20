/* =========================================
   SmartWaste - Main JavaScript
   ========================================= */


document.addEventListener("DOMContentLoaded", function () {

    console.log("SmartWaste JavaScript loaded successfully.");



    /* -----------------------------------------
       Auto Hide Django Messages
       ----------------------------------------- */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "opacity 0.5s ease";

            alert.style.opacity = "0";

            setTimeout(function () {

                alert.remove();

            }, 500);

        }, 4000);

    });



    /* -----------------------------------------
       Confirm Logout
       ----------------------------------------- */

    const logoutLinks = document.querySelectorAll(
        'a[href*="/logout/"]'
    );


    logoutLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const confirmLogout = confirm(
                "Are you sure you want to logout?"
            );


            if (!confirmLogout) {

                event.preventDefault();

            }

        });

    });

});

/* -----------------------------------------
   Waste Image Preview
   ----------------------------------------- */

const imageInput = document.getElementById(
    "uploaded_image"
);

const imagePreview = document.getElementById(
    "imagePreview"
);

const imagePreviewContainer = document.getElementById(
    "imagePreviewContainer"
);


if (imageInput) {

    imageInput.addEventListener(
        "change",
        function () {

            const file = this.files[0];


            if (file) {

                const reader = new FileReader();


                reader.onload = function (event) {

                    imagePreview.src =
                        event.target.result;

                    imagePreviewContainer.style.display =
                        "block";

                };


                reader.readAsDataURL(file);

            }

        }
    );

}

/* =========================================
   SmartWaste - Webcam Detection
   ========================================= */

const webcam = document.getElementById("webcam");
const canvas = document.getElementById("canvas");
const capturedImage = document.getElementById("capturedImage");

const startCameraButton = document.getElementById("startCamera");
const captureImageButton = document.getElementById("captureImage");

let cameraStream = null;


/* -----------------------------------------
   Open Camera
   ----------------------------------------- */

if (startCameraButton) {

    startCameraButton.addEventListener("click", async function () {

        try {

            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            });

            webcam.srcObject = cameraStream;

            webcam.style.display = "block";

            captureImageButton.style.display = "inline-block";

            startCameraButton.style.display = "none";

        } catch (error) {

            console.error("Camera Error:", error);

            alert(
                "Camera access was denied or the camera is not available."
            );

        }

    });

}


/* -----------------------------------------
   Capture Image
   ----------------------------------------- */

if (captureImageButton) {

    captureImageButton.addEventListener("click", function () {

        const context = canvas.getContext("2d");

        canvas.width = webcam.videoWidth;
        canvas.height = webcam.videoHeight;

        context.drawImage(
            webcam,
            0,
            0,
            canvas.width,
            canvas.height
        );

        capturedImage.src = canvas.toDataURL("image/jpeg");

        capturedImage.style.display = "block";

    });

}