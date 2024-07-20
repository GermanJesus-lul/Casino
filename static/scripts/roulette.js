// Retrieves the spin button and the roulette wheel image elements from the DOM.
let spinButton = document.getElementById("spin");
let wheel = document.getElementById("wheel_img");

// Maps roulette numbers to their corresponding positions on the wheel image.
const numberToPositionIndex = [0, 14, 32, 2, 34, 18, 27, 6, 21, 10, 19, 23, 4, 25, 12, 36, 16, 30, 8, 35, 13, 33, 9, 20, 17, 31, 1, 26, 5, 7, 22, 11, 37, 15, 29, 3, 24, 28]

/**
 * Initiates a spin on the roulette wheel.
 * Disables the spin button to prevent multiple requests, checks the user's balance,
 * and sends a POST request to the server with the bet details.
 * Upon receiving the result, it animates the wheel to the result position.
 */
async function spin() {
    spinButton.disabled = true;
    updateUserdata();
    if (parseInt(document.getElementById("balance").innerText) < parseInt(document.getElementById("bet").value)) {
        alert("You don't have enough balance to make this bet.");
        spinButton.disabled = false;
    } else if (document.getElementById("bet").value < 1) {
        alert("Bet must be greater than 0.");
        spinButton.disabled = false;
    } else {
        wheel.classList.add("spinning_wait");
        wheel.addEventListener("animationend", restartSpinningWait);
        const timeoutPromise = new Promise(resolve => setTimeout(resolve, 2000));
        const fetchPromise = fetch("/roulette/spin", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "bet": document.getElementById("bet").value,
                "type": document.getElementById("bet-type").value,
                "choice": document.querySelector('input[name="choice"]:not([style*="display: none"]):checked') ? document.querySelector('input[name="choice"]:checked').value : null,
                "number": document.getElementById("number").style.display !== "none" ? document.getElementById("number").value : null
            })
            // "choice": choice
        }).then(response => response.text());

        Promise.all([fetchPromise, timeoutPromise]).then(async (values) => {
            const result = parseInt(values[0]);
            if (isNaN(result)) {
                alert(values[0]);
                spinButton.disabled = false;
            } else {
                const positionIndex = numberToPositionIndex[result];
                const targetDeg = positionIndex * 9.473684210526316;
                wheel.style.setProperty("--target-deg", `${targetDeg + (2 * 360)}deg`);
                wheel.removeEventListener("animationend", restartSpinningWait);
                wheel.addEventListener("animationend", function () {
                    wheel.classList.remove("spinning_wait");
                    void wheel.offsetWidth;
                    wheel.classList.add("spinning");
                    wheel.addEventListener("animationend", function () {
                        updateUserdata();
                        wheel.style.transform = `rotate(${targetDeg}deg)`;
                        wheel.classList.remove("spinning");
                        wheel.style.setProperty("--start-deg", `${targetDeg}deg`);
                        wheel.style.setProperty("--target-wait-deg", `${targetDeg + 360}deg`);
                        spinButton.disabled = false;
                    }, {once: true});
                }, {once: true});
            }
        });
    }
}

// Adds an event listener to the spin button to initiate the spin process.
spinButton.addEventListener('click', spin);

/**
 * Restart the spinning animation.
 * This function is called after the spinning animation ends.
 */
function restartSpinningWait() {
    wheel.classList.remove("spinning_wait");
    void wheel.offsetWidth;
    wheel.classList.add("spinning_wait");
}

/**
 * Updates the input container based on the selected bet type.
 * This function dynamically changes the input fields to match the bet type selected by the user.
 * It supports three bet types: color, even/odd, and number. Based on the selection,
 * it displays the relevant input fields and hides the others.
 *
 * For the 'color' bet type, it checks the 'red' radio button by default and clears the number input.
 * For the 'evenodd' bet type, it checks the 'even' radio button by default and clears the number input.
 * For the 'number' bet type, it sets the number input's value to 10 and unchecks all choice radio buttons.
 */
function updateInputContainer() {
    const selectedType = document.getElementById('bet-type').value;
    const colorInputs = document.getElementById('colorInputs');
    const evenOddInputs = document.getElementById('evenOddInputs');
    const numberInput = document.getElementById('numberInput');

    // Initially hide all elements
    colorInputs.style.display = 'none';
    evenOddInputs.style.display = 'none';
    numberInput.style.display = 'none';

    // Display the appropriate element based on the selected bet type
    if (selectedType === 'color') {
        document.getElementById('red').checked = true;
        colorInputs.style.display = 'block';
        document.getElementById('number').value = null;
    } else if (selectedType === 'evenodd') {
        document.getElementById('even').checked = true;
        evenOddInputs.style.display = 'block';
        document.getElementById('number').value = null;
    } else if (selectedType === 'number') {
        document.getElementById('number').value = 10;
        numberInput.style.display = 'block';
        Array.from(document.getElementsByClassName('choice-radio-button')).forEach(radio => {
            radio.checked = false;
        })
    }
}

// Initializes the input container and wheel properties when the document is loaded.
document.addEventListener('DOMContentLoaded', updateInputContainer);
document.addEventListener('DOMContentLoaded', function () {
    wheel.style.setProperty("--start-deg", "0deg");
    wheel.style.setProperty("--target-wait-deg", "360deg");
})

// Updates the input container when the bet type is changed.
document.getElementById('bet-type').addEventListener('change', updateInputContainer);