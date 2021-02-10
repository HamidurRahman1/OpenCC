document.querySelectorAll(".modal").forEach((m) => (m.style.display = "none"));

document.querySelectorAll(".modal-trigger").forEach((t) => {
  t.onclick = () => {
    document.querySelector(`#${t.getAttribute("target")}`).style.display =
      "block";
  };
});

document.querySelectorAll(".modal-close-btn").forEach((t) => {
  t.onclick = () => {
    document.querySelector(`#${t.getAttribute("target")}`).style.display =
      "none";
  };
});

export const showModal = (id, content) => {
    document.querySelector(id).style.display = 'block';
    document.querySelector(`${id} .content p`).innerText = content;
}
