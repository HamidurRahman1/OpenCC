
const buttons = document.querySelectorAll('.accordion__button');
const contentSections = document.querySelectorAll('.accordion__content');

function setInitialAriaValue(elements, aria, ariaValue) {
    elements.forEach((element) => {
        element.setAttribute(`${aria}`, `${ariaValue}`);
    });
}

function accordionToggleHandler() {
    buttons.forEach((button) => {
        button.addEventListener('click', toggleContent);
    });
}

function toggleContent(e) {
    toggleButton(e.target);
    toggleDetails(e.target);
}

function toggleButton(button) {
    const expandedValue = button.getAttribute('aria-expanded');
    const setValue = expandedValue === 'true' ? 'false' : 'true';
    button.setAttribute('aria-expanded', setValue);
}

function toggleDetails(button) {
    const buttonAriaControl = button.getAttribute('aria-controls');
    const content = document.getElementById(buttonAriaControl);
    const hiddenValue = content.getAttribute('aria-hidden');
    const setValue = hiddenValue === 'true' ? 'false' : 'true';
    content.setAttribute('aria-hidden', setValue);
}

setInitialAriaValue(buttons, 'aria-expanded', 'false');
setInitialAriaValue(contentSections, 'aria-hidden', 'true');
accordionToggleHandler();