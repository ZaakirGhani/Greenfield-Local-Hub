

//high contrast
const contrastToggle = document.getElementById('contrast-toggle');

const applyContrast = (isHigh) => {
    document.body.classList.toggle('high-contrast', isHigh);

    if (contrastToggle) {
        contrastToggle.checked = isHigh;
    }
};

const stateSaved = localStorage.getItem('highContrast') === 'true';
applyContrast(stateSaved);


if(contrastToggle) {
    contrastToggle.addEventListener('click', () => {
        const newStateSaved = !document.body.classList.contains('high-contrast');
        localStorage.setItem('highContrast', newStateSaved);
        applyContrast(newStateSaved);
    });
};

//Vertical scroller
//Container this is the container based on the css class .products
let productsContainer = document.querySelector('.products')
//This is right and left id button
let btnLeft = document.getElementById('left-arrow')
let btnRight = document.getElementById('right-arrow')


productsContainer.addEventListener('wheel', (event) => {
    event.preventDefault();
    productsContainer.scrollBy({
        left: event.deltaY,
        behavior: 'smooth'

        });
});

//When clicking on the left arrow button go scroll left.
btnLeft.addEventListener('click', () => {
    productsContainer.scrollBy({
        left: -900,
        behavior: 'smooth'
    });
});

//When clicking on the left arrow button go scroll right.
btnRight.addEventListener('click', () => {
    productsContainer.scrollBy({
        left: 900,
        behavior: 'smooth'
    });
});
