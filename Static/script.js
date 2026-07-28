// ==============================
// AI Movie Search Autocomplete
// ==============================

const input = document.getElementById("movie");
const suggestionBox = document.getElementById("suggestions");

if (input) {

    input.addEventListener("keyup", function () {

        const query = input.value.trim();

        if (query.length < 2) {

            suggestionBox.innerHTML = "";
            return;

        }

        fetch("/autocomplete?q=" + encodeURIComponent(query))

            .then(response => response.json())

            .then(data => {

                suggestionBox.innerHTML = "";

                if (data.length === 0) {

                    return;

                }

                data.forEach(movie => {

                    const div = document.createElement("div");

                    div.className = "suggestion";

                    div.innerHTML =
                        '<i class="fa-solid fa-film"></i> ' + movie;

                    div.onclick = function () {

                        input.value = movie;

                        suggestionBox.innerHTML = "";

                    };

                    suggestionBox.appendChild(div);

                });

            });

    });

    // Hide suggestions when clicking elsewhere
    document.addEventListener("click", function (e) {

        if (e.target !== input) {

            suggestionBox.innerHTML = "";

        }

    });

}