// helpers.js

export function getCookie(name) {
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
    const firstSegment = window.location.pathname.split('/')[1];
    const urlToFetch = window.location.origin + '/' + firstSegment + '/' + url;
    return fetch(urlToFetch, {
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
      duration: 4000,
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

export const DAYS_OF_WEEK = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
export const MONTHS_OF_YEAR = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

export function addDays(days = 1, data) {
    const date = new Date(data.year, data.month, data.day);
    date.setDate(date.getDate() + days);

    return {
        day: date.getDate(),
        month: date.getMonth(),
        year: date.getFullYear(),
        dayOfWeek: date.getDay()
    };
}

export function subtractDays(days = 1, data) {
    return addDays(-days, data);
}

export function addMinutesToDate(date, minutes) {
    return new Date(date.getTime() + minutes * 60000);
}

/**
 * Ajusta la hora de un input datetime-local al intervalo más cercano basado en el porcentaje proporcionado.
 * @param {Event} event - El evento del input datetime-local.
 * @param {number} percentage - El porcentaje de hora para redondear (por ejemplo, .5 para media hora, .25 para 15 minutos).
 */
export function adjustTimeToNearestInterval(event, percentage) {
    const input = event.target;
    const value = input.value;

    if (value) {
        const date = new Date(value);
        const minutes = date.getMinutes();
        const interval = percentage * 60; // Convertir el porcentaje a minutos
        const adjustedMinutes = Math.round(minutes / interval) * interval;
        date.setMinutes(adjustedMinutes);

        // Formatear la fecha y hora en el formato local sin convertir a UTC
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const adjustedMinutesStr = String(date.getMinutes()).padStart(2, '0');

        input.value = `${year}-${month}-${day}T${hours}:${adjustedMinutesStr}`;
    }
}