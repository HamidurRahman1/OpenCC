const add_request_form = document.querySelector('#add-request');
let formData;
add_request_form.onsubmit = evt => {
  evt.preventDefault();
  formData = new FormData(add_request_form);
  requestInfo = {
    "phone-number" : formData.get('phone-number'),
    "term" : formData.get('term'),
    "subject" : formData.get('subject'),
    "class-num-5" : formData.get('class-num-5'),
  }
  fetch('/api/request', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestInfo)
  })
  .then(response => response.json())
  .then(data => console.log(data));
}