const diseaseForm =
    document.getElementById("diseaseForm");

const cropImage =
    document.getElementById("cropImage");

const imagePreview =
    document.getElementById("imagePreview");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");



/* =====================================================
   IMAGE PREVIEW
===================================================== */

cropImage.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }


    const reader =
        new FileReader();


    reader.onload = function (event) {

        imagePreview.style.display =
            "block";


        imagePreview.innerHTML = `

            <img
                src="${event.target.result}"
                alt="Crop Preview">

        `;

    };


    reader.readAsDataURL(file);

});



/* =====================================================
   SEND IMAGE TO PYTHON AI API
===================================================== */

diseaseForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const file =
            cropImage.files[0];


        if (!file) {

            alert(
                "Please select a crop image."
            );

            return;

        }


        const formData =
            new FormData();


        formData.append(
            "image",
            file
        );


        loading.style.display =
            "block";


        result.style.display =
            "none";


        try {

            /*
             * CHANGE THIS URL IF YOUR
             * PYTHON API USES A DIFFERENT PORT.
             */

            const response =
                await fetch(
                    "http://localhost:8000/predict",
                    {
                        method: "POST",

                        body: formData
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Server error"
                );

            }


            const data =
                await response.json();


            showResult(data);


        }

        catch (error) {

            console.error(error);


            alert(
                "Could not connect to the crop disease detection server."
            );

        }

        finally {

            loading.style.display =
                "none";

        }

    }
);



/* =====================================================
   DISPLAY RESULT
===================================================== */

function showResult(data) {

    result.style.display =
        "block";


    document.getElementById(
        "diseaseName"
    ).textContent =
        data.disease;


    const confidence =
        Number(data.confidence);


    document.getElementById(
        "confidence"
    ).textContent =
        confidence + "%";


    document.getElementById(
        "confidenceFill"
    ).style.width =
        confidence + "%";


    document.getElementById(
        "recommendationText"
    ).textContent =
        data.recommendation ||
        "Please consult an agricultural expert for further treatment advice.";

}