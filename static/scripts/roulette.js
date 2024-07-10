let spinButton = document.getElementById("spin");
let redButton = document.getElementById("red");
let blackButton = document.getElementById("black");
let wheel = document.getElementById("wheel_img");

const numberToPositionIndex = [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 37, 34, 17, 25, 2, 21, 4, 19, 15, 32]

let choice = "red"

async function spin() {
    const timeoutPromise = new Promise(resolve => setTimeout(resolve, 2000));
    const fetchPromise = fetch("/roulette/spin", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "bet": document.getElementById("bet").value,
            "choice": choice
        })
    }).then(response => response.text());

    Promise.all([fetchPromise, timeoutPromise]).then(async (values) => {
        const positionIndex = parseInt(values[0]);
        const result = numberToPositionIndex[positionIndex];
        const targetDeg = result * 9.473684210526316;
        wheel.style.setProperty("--target-deg", `${targetDeg + (3*360)}deg`);
        wheel.classList.add("spinning");
        wheel.addEventListener("animationend", function () {
            wheel.style.transform = `rotate(${result * 9.473684210526316}deg)`;
            wheel.classList.remove("spinning");
            wheel.style.setProperty("--start-deg", `${targetDeg}deg`);
        } , {once: true});
        updateUserdata();
    });
}

redButton.addEventListener("click", function () {
    choice = "red"
})
blackButton.addEventListener("click", function () {
    choice = "black"
})
spinButton.addEventListener('click', spin);