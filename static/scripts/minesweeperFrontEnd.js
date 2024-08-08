// Referenz zur grid-container-Div erhalten
const gridContainer = document.getElementById('grid-container');

function buttonClicked(number) {
    console.log("Button " + number + " wurde gedrückt");
}

// Buttons dynamisch erzeugen und Event Listener hinzufügen
for (let i = 0; i < 25; i++) {
    const button = document.createElement('button');
    button.textContent = i.toString();
    button.addEventListener('click', () => buttonClicked(i));

    const gridItem = document.createElement('div');
    gridItem.classList.add('grid-item');
    gridItem.appendChild(button);

    gridContainer.appendChild(gridItem);
}