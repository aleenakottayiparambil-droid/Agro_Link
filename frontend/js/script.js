/* =====================================================
   AGROLINK JAVASCRIPT
===================================================== */


/* =====================================================
   LOGIN
===================================================== */

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener("submit", function (event) {

        event.preventDefault();


        const email =
            document.getElementById("loginEmail").value;

        const role =
            document.getElementById("loginRole").value;


        if (!role) {

            alert("Please select your role.");

            return;

        }


        /*
        Temporary frontend login.

        Later this will be replaced with:
        fetch("http://localhost:5000/api/login", ...)
        */


        localStorage.setItem(
            "agrolinkUser",
            JSON.stringify({

                name: email.split("@")[0],

                email: email,

                role: role

            })
        );


        window.location.href =
            "dashboard.html";

    });

}


/* =====================================================
   REGISTRATION ROLE SELECTION
===================================================== */

const roleCards =
    document.querySelectorAll(".role-card");


const registerRole =
    document.getElementById("registerRole");


const registerTitle =
    document.getElementById("registerTitle");


const registerButton =
    document.getElementById("registerButton");


roleCards.forEach(function (card) {

    card.addEventListener("click", function () {


        roleCards.forEach(function (item) {

            item.classList.remove("selected");

        });


        card.classList.add("selected");


        const role =
            card.getAttribute("data-role");


        registerRole.value =
            role;


        registerTitle.textContent =
            "Create " +
            role.charAt(0).toUpperCase() +
            role.slice(1) +
            " Account";


        registerButton.disabled =
            false;

    });

});


/* =====================================================
   REGISTRATION FORM
===================================================== */

const registerForm =
    document.getElementById("registerForm");


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const name =
                document.getElementById(
                    "registerName"
                ).value;


            const email =
                document.getElementById(
                    "registerEmail"
                ).value;


            const phone =
                document.getElementById(
                    "registerPhone"
                ).value;


            const password =
                document.getElementById(
                    "registerPassword"
                ).value;


            const role =
                document.getElementById(
                    "registerRole"
                ).value;


            if (!role) {

                alert(
                    "Please select Farmer, Consumer or Retailer."
                );

                return;

            }


            /*
            Temporary frontend registration.

            Later this data should be sent
            to your backend API.
            */


            const user = {

                name: name,

                email: email,

                phone: phone,

                password: password,

                role: role

            };


            localStorage.setItem(
                "agrolinkUser",
                JSON.stringify(user)
            );


            alert(
                "Account created successfully!"
            );


            window.location.href =
                "dashboard.html";

        }
    );

}


/* =====================================================
   DASHBOARD
===================================================== */

const dashboardNav =
    document.getElementById("dashboardNav");


if (dashboardNav) {

    loadDashboard();

}


function loadDashboard() {


    const storedUser =
        localStorage.getItem(
            "agrolinkUser"
        );


    if (!storedUser) {

        window.location.href =
            "login.html";

        return;

    }


    const user =
        JSON.parse(storedUser);


    const userName =
        document.getElementById(
            "userName"
        );


    const userRole =
        document.getElementById(
            "userRole"
        );


    const dashboardTitle =
        document.getElementById(
            "dashboardTitle"
        );


    userName.textContent =
        user.name;


    userRole.textContent =
        user.role;


    dashboardTitle.textContent =
        user.role.charAt(0).toUpperCase() +
        user.role.slice(1) +
        " Dashboard";


    const farmerDashboard =
        document.getElementById(
            "farmerDashboard"
        );


    const buyerDashboard =
        document.getElementById(
            "buyerDashboard"
        );


    if (user.role === "farmer") {

        farmerDashboard.classList.add(
            "active"
        );


        dashboardNav.innerHTML = `

            <a href="#" class="active">
                🏠 Dashboard
            </a>

            <a href="#" onclick="openFeature('Sell Produce')">
                🌾 Sell Produce
            </a>

            <a href="#" onclick="openFeature('Government Schemes')">
                🏛️ Government Schemes
            </a>

            <a href="#" onclick="openFeature('Crop Disease Detection')">
                🔬 Crop Disease
            </a>

            <a href="#" onclick="openFeature('Weather')">
                ☀️ Weather
            </a>

        `;

    }


    else if (
        user.role === "consumer" ||
        user.role === "retailer"
    ) {

        buyerDashboard.classList.add(
            "active"
        );


        const buyerType =
            document.getElementById(
                "buyerType"
            );


        buyerType.textContent =
            user.role.toUpperCase() +
            " MARKETPLACE";


        dashboardNav.innerHTML = `

            <a href="#" class="active">
                🏠 Dashboard
            </a>

            <a href="#" onclick="openFeature('Buy Produce')">
                🛒 Buy Produce
            </a>

        `;

    }

}


/* =====================================================
   FEATURE BUTTON
===================================================== */

function openFeature(feature) {

    alert(
        feature +
        " module will open here.\n\n" +
        "This can later be connected to your backend."
    );

}


/* =====================================================
   LOGOUT
===================================================== */

function logout() {

    localStorage.removeItem(
        "agrolinkUser"
    );


    window.location.href =
        "index.html";

}