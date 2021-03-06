import * as modal from "./modal.js";

const add_request_form = document.querySelector('#add-request');
let formData, requestInfo;
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
  .then(data => 
    {
      if('success' in data){
        modal.showModal('#sucess-modal', data[Object.keys(data)[0]]);
        add_request_form.reset();
      }
      else
        modal.showModal('#error-modal', data[Object.keys(data)[0]])
    }
  );
}