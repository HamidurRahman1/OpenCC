let hamburger = document.querySelector('.nav-burger');
let visible = false;
let navContainer = document.querySelector('.nav-links');
hamburger.onclick = () => {
    navContainer.style.display = visible ? 'none' : 'flex';
    visible = !visible;
}
document.onclick = (e) => {
    if(!hamburger.contains(e.target) && window.innerWidth <= 768) {
        navContainer.style.display = 'none';
        visible = !visible;
    }
}

window.addEventListener('resize', () => {
    if ( window.innerHeight > 768 && !visible){
        navContainer.style.display = visible ? 'none' : 'flex';
        visible = !visible; 
    }
})