let spinButton = document.getElementById("spin");
let wheel = document.getElementById("wheel_img");
let ball = document.getElementById("ball_img");

const numberToPositionIndex = [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 37, 34, 17, 25, 2, 21, 4, 19, 15, 32]

let choice = "red"

async function spin() {
    spinButton.disabled = true;
    updateUserdata();
    if (document.getElementById("balance").innerText < document.getElementById("bet").value) {
        alert("You don't have enough balance to make this bet.");
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
            const positionIndex = parseInt(values[0]);
            const result = numberToPositionIndex[positionIndex];
            const targetDeg = result * 9.473684210526316;
            wheel.style.setProperty("--target-deg", `${targetDeg + (2 * 360)}deg`);
            wheel.removeEventListener("animationend", restartSpinningWait);
            wheel.addEventListener("animationend", function () {
                wheel.classList.remove("spinning_wait");
                void wheel.offsetWidth;
                wheel.classList.add("spinning");
                wheel.addEventListener("animationend", function () {
                    wheel.style.transform = `rotate(${result * 9.473684210526316}deg)`;
                    wheel.classList.remove("spinning");
                    wheel.style.setProperty("--start-deg", `${targetDeg}deg`);
                    wheel.style.setProperty("--target-wait-deg", `${targetDeg + 360}deg`);
                    updateUserdata();
                    spinButton.disabled = false;
                }, {once: true});
            }, {once: true});
        });
    }
}

spinButton.addEventListener('click', spin);

function restartSpinningWait() {
    wheel.classList.remove("spinning_wait");
    void wheel.offsetWidth;
    wheel.classList.add("spinning_wait");
}

function updateInputContainer() {
    var selectedType = document.getElementById('bet-type').value;
    var inputContainer = document.getElementById('input-container');

    inputContainer.innerHTML = ''; // Vorherige Eingaben löschen

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

document.addEventListener('DOMContentLoaded', updateInputContainer);
document.addEventListener('DOMContentLoaded', function () {
    wheel.style.setProperty("--start-deg", "0deg");
    wheel.style.setProperty("--target-wait-deg", "360deg");
})

document.getElementById('bet-type').addEventListener('change', updateInputContainer);