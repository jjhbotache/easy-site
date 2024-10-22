// helpers.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprueba si el cookie comienza con el nombre del token
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

export async function myFetch(url = '', data = {}, method = 'POST') {
  return fetch(url, {
    method: method, // Método de la solicitud
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken  // Aquí incluimos el token CSRF
    },
    body: method === 'GET' ? null : JSON.stringify(data) // Datos a enviar
  })
  .then(response => response.json()) // Respuesta en formato JSON
  .catch(error => console.error('Error:', error));
}


/**
 * 
 * @param {string} type - The type of alert to show. Can be 'warning', 'error', 'success', 'info'
 * @param {string} message - The message to show in the alert
 */
export function showAlert(type = "warning", message) {
  let backgroundColor;
    switch (type) {
            case 'success':
                    backgroundColor = "#28a745"; // Green
                    break;
            case 'error':
                    backgroundColor = "#dc3545"; // Red
                    break;
            case 'info':
                    backgroundColor = "#17a2b8"; // Blue
                    break;
            case 'warning':
            default:
                    backgroundColor = "#ffc107"; // Yellow
                    break;
    }

  Toastify({
      text: message,
      duration: 6000,
      close: true,
      gravity: "top", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      style: {
          background: backgroundColor,
          zIndex: 99999,
      },
      onClick: function(){} // Callback after click
  }).showToast();
}
