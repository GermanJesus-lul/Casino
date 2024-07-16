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
                "choice": document.querySelector('input[name="choice"]:checked') ? document.querySelector('input[name="choice"]:checked').value : null,
                "number": document.getElementById("number") ? document.getElementById("number").value : null
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
 * Dynamically changes the input fields to match the bet type (color, even/odd, number).
 */
function updateInputContainer() {
    const selectedType = document.getElementById('bet-type').value;
    const inputContainer = document.getElementById('input-container');

    inputContainer.innerHTML = '';

    if (selectedType === 'color') {
        inputContainer.innerHTML = `
            <label class="choice-radio-label"><input class="choice-radio-button" type="radio" value="red" id="red" name="choice" checked="checked"> Red</label>
            <label class="choice-radio-label"><input class="choice-radio-button" type="radio" value="black" id="black" name="choice"> Black</label>
        `;
    } else if (selectedType === 'evenodd') {
        inputContainer.innerHTML = `
            <label class="choice-radio-label"><input class="choice-radio-button" type="radio" value="even" id="even" name="choice" checked="checked"> Even</label>
            <label class="choice-radio-label"><input class="choice-radio-button" type="radio" value="odd" id="odd" name="choice"> Odd</label>
        `;
    } else if (selectedType === 'number') {

        inputContainer.innerHTML = `
            <div style="display: inline">
                <button type="button" class="input-number-button"
                        onclick="this.parentNode.querySelector('[type=number]').stepDown();">
                    -
                </button>
                <input id="number" type="number" min="0" max="36" step="1" value="0"/>
                <button type="button" class="input-number-button"
                        onclick="this.parentNode.querySelector('[type=number]').stepUp();">
                    +
                </button>
            </div>
        `;
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