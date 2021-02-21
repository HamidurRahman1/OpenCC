const WRAPPERS = document.querySelectorAll(".wrapper");
WRAPPERS.forEach((w) => (w.style.display = "none"));

document.querySelector("#home-wrapper").style.display = "block";

const NAV_ITEMS = document.querySelectorAll(".link");
NAV_ITEMS.forEach((n) => {
  n.onclick = () => {
    WRAPPERS.forEach(w => w.style.display  = n.getAttribute("value") == w.id ? 'block' : 'none');
  };
});