import { myFetch, showAlert, DAYS_OF_WEEK, MONTHS_OF_YEAR, addDays, subtractDays, adjustTimeToNearestInterval, addMinutesToDate } from "./helpers.js";


// Elements
const calendar_config = JSON.parse(document.getElementById('calendar_config').textContent, (key, value) => {
    if (key === 'appointment_start_time' || key === 'appointment_end_time') {
        return parseInt(value);
    }
    return value;
});

console.log(calendar_config);

const appointments = JSON.parse(document.getElementById('appointments').textContent, (key, value) => {
    if (key === 'start_datetime' || key === 'end_datetime') {
        return new Date(value);
    }
    return value;
});
// Create pseudoId for each appointment
appointments.forEach(appointment => {
    const start = appointment.start_datetime;
    const end = appointment.end_datetime;
    const startMinutes = start.getUTCHours() * 60 + start.getMinutes();
    const endMinutes = end.getUTCHours() * 60 + end.getMinutes();
    
    const pseudoId = `${start.getFullYear()}-${String(start.getMonth() + 1).padStart(2, '0')}-${String(start.getDate()).padStart(2, '0')}-${startMinutes}-${endMinutes}`;
    appointment.pseudoId = pseudoId;
});
console.log(appointments);

const is_admin = JSON.parse(document.getElementById('is_admin').textContent)
console.log(is_admin);


const headerDay1 = document.querySelector('#headerDay1');
const headerDay2 = document.querySelector('#headerDay2');
const headerDay3 = document.querySelector('#headerDay3');
const headers = [headerDay1, headerDay2, headerDay3];
const prevDaysBtn = document.getElementById('prevDaysBtn');
const nextDaysBtn = document.getElementById('nextDaysBtn');

const todayBtn = document.getElementById('todayBtn');

// Modal Elements
const eventModal = document.querySelector('#eventModal');
const appointmentEditor = eventModal.querySelector('#appointmentEditor');

const addEventBtn = document.querySelector('#addEventBtn');
const closeModalBtn = appointmentEditor.querySelector('#closeModalBtn');
const deleteEventBtn = appointmentEditor.querySelector('#deleteEventBtn');

// Current Date
const currentDate = new Date();
const currentDay = currentDate.getDate();
const currentMonth = currentDate.getMonth();
const currentYear = currentDate.getFullYear();
const currentHour = currentDate.getHours();
const currentDayOfWeek = currentDate.getDay();

// Calendar Data
const dataOnCalendar = {
    day: currentDay,
    month: currentMonth,
    year: currentYear,
    dayOfWeek: currentDayOfWeek
};

function main() {
    scrollToCurrentHour()

    // for all the .hourBox, according to the current to the calendar_config.appointment_duration, add mini boxes
    syncMiniBoxesToHours();
    syncDataOnCalendar(dataOnCalendar);
    addEventListeners();

    document.querySelector('#footerSecction')?.remove();
}

function syncMiniBoxesToHours() {
    const hourBoxes = document.querySelectorAll('.hourBox');
    const durationInMinutes = calendar_config.appointment_duration * 60;
    const amountOfMiniBoxes = Math.floor(1 / calendar_config.appointment_duration);
    
    const template = document.getElementById('miniHourBox').content;
    const templateBusy = document.getElementById('miniHourBoxBusy').content;
    const templateOff = document.getElementById('miniHourBoxOff').content;
    hourBoxes.forEach((hourBox) => {
        const [dayPart, hourPart] = hourBox.id.split('Hour');
        const hour = parseInt(hourPart);
        const dayIndex = parseInt(dayPart.split('day')[1]) - 1;
        const day = parseInt(headers[dayIndex].querySelector('.day').textContent);
        const dayOfWeek = (new Date(dataOnCalendar.year, dataOnCalendar.month, day).getDay() + 6) % 7 + 1; // Ajustar para que empiece desde lunes
    
        hourBox.innerHTML = ""; // Limpiar el hourBox
    
        const isOffTime = hour < calendar_config.appointment_start_time || hour >= calendar_config.appointment_end_time || calendar_config.off_hours.includes(hour);
        const isOffDay = calendar_config.off_days_of_the_week.includes(dayOfWeek);
    
        for (let i = 0; i < amountOfMiniBoxes; i++) {
            const startMinute = hour * 60 + (i * durationInMinutes);
            const endMinute = startMinute + durationInMinutes - 1;
    
            const miniBoxData = {
                hour: hour,
                hourIndex: i,
                day: day,
                weekDay: dayOfWeek,
                month: dataOnCalendar.month,
                year: dataOnCalendar.year,
                startMinute: startMinute,
                endMinute: endMinute
            };
            
    
            
    
            let miniBox;
            
            // obtener los milisegundos desde la epoca absoluta
            const today = new Date();
            const todayMilliseconds = today.getTime(); 

            const appointmentStartTimeInMinutes = Math.abs( (hour * 60) - startMinute);
            const appointmentEndTimeInMinutes = Math.abs( (hour * 60) - endMinute);
            const miniBoxDateEnd = new Date(
                miniBoxData.year,
                miniBoxData.month,
                miniBoxData.day,
                hour,
                appointmentEndTimeInMinutes
            );
            const miniBoxDateStart = new Date(
                miniBoxData.year,
                miniBoxData.month,
                miniBoxData.day,
                hour,
                appointmentStartTimeInMinutes
            );

            const miniBoxTimestamp = miniBoxDateStart.getTime();
            const miniBoxIsInThePast = miniBoxTimestamp < todayMilliseconds;
            
            const existingAppointment = appointments.find(appointment => 
                appointment.start_datetime < miniBoxDateEnd &&
                appointment.end_datetime > miniBoxDateStart 
            );  
            

            

            if (isOffTime || isOffDay ||  miniBoxIsInThePast) {
                miniBox = document.importNode(templateOff, true).firstElementChild;
            } else if (existingAppointment) {
                miniBox = document.importNode(templateBusy, true).firstElementChild;
                
                is_admin && miniBox.addEventListener('click', () => { 
                    setAppointmentDataInEditor(existingAppointment); 
                    eventModal.show(); 
                });
            } else {
                miniBox = document.importNode(template, true).firstElementChild;
                // when clicked, set the start and end time in the form
                miniBox.addEventListener('click', () => {
                    
                    // Convertir a naive eliminando la información de la zona horaria
                    const naiveStartDate = new Date(miniBoxDateStart.getTime() - (miniBoxDateStart.getTimezoneOffset() * 60000));
                    const naiveEndDate = new Date(miniBoxDateEnd.getTime() - (miniBoxDateEnd.getTimezoneOffset() * 60000));
                
                    appointmentEditor.start_datetime.value = naiveStartDate.toISOString().slice(0, 16);
                    appointmentEditor.end_datetime.value = naiveEndDate.toISOString().slice(0, 16);
                    eventModal.show();
                });
            }
    
            miniBox.setAttribute('data-info', JSON.stringify(miniBoxData));
            hourBox.appendChild(miniBox);
        }
    });
}

function syncDataOnCalendar(givenData = dataOnCalendar) {
    headers.forEach((header, index) => {
        const dayElement = header.querySelector('.day');
        const weekDayElement = header.querySelector('.weekDay');
        const newDate = addDays(index, givenData);

        updateHeaderStyles(dayElement, weekDayElement, newDate);
        updateHeaderContent(dayElement, weekDayElement, newDate);
    });
    syncMiniBoxesToHours();

    // update the month and year
    window.month.textContent = MONTHS_OF_YEAR[givenData.month];
    window.year.textContent = givenData.year;
}

function updateHeaderStyles(dayElement, weekDayElement, newDate) {
    if (newDate.day === currentDay && newDate.month === currentMonth && newDate.year === currentYear) {
        dayElement.classList.add('secondary-light-bg');
        weekDayElement.classList.add('primary-dark-color');
    } else {
        dayElement.classList.remove('secondary-light-bg');
        weekDayElement.classList.remove('primary-dark-color');
    }
}

function updateHeaderContent(dayElement, weekDayElement, newDate) {
    dayElement.textContent = newDate.day;
    weekDayElement.textContent = DAYS_OF_WEEK[newDate.dayOfWeek];
}

function updateCalendar(days) {
    const newDate = days > 0 ? addDays(days, dataOnCalendar) : subtractDays(-days, dataOnCalendar);
    Object.assign(dataOnCalendar, newDate);
    syncDataOnCalendar(dataOnCalendar);
}


async function handleAppointmentSubmission (capchaToken) {
    const appointmentForm = document.querySelector('#appointmentEditor');
    
    
    const formData = new FormData(appointmentForm);
    const data = Object.fromEntries(formData.entries());
    data['g-recaptcha-response'] = capchaToken || '';

    // Verificar que todos los campos requeridos estén completos
    if (!data.full_name || !data.start_datetime || !data.end_datetime) {
        showAlert('error', 'Por favor, complete todos los campos requeridos.');
        return;
    }

    // Convertir las fechas a cadenas ISO completas con la zona horaria local del cliente
    const startDate = new Date(data.start_datetime);
    const endDate = new Date(data.end_datetime);

    data.start_datetime = startDate.toISOString();
    data.end_datetime = endDate.toISOString();

    try {
        const method = data.event_id ? 'PUT' : 'POST';
        const response = await myFetch('create-appointment/', data, method);
        if (response.status === 'success') {
            showAlert('success', `¡Cita ${method === 'POST' ? 'creada' : 'actualizada'} exitosamente!`);
            appointmentForm.reset(); // Limpiar el formulario después de la creación/actualización exitosa
            eventModal.close();
            setTimeout(() => { window.location.reload(); }, 1000);
        } else {
            !!response.message.__all__ 
                ? showAlert('error', `Error: ${response.message.__all__.join('\n')}`)   
                : showAlert('error', `Error: ${response.message}`);
            console.log(response);
        }
    } catch (error) {
        showAlert('error', `Error: ${error}`);
    }
};
window.handleAppointmentSubmission = handleAppointmentSubmission;

function addModalEventListeners() {
    addEventBtn.addEventListener('click', () => {
        eventModal.show();
    });

    closeModalBtn.addEventListener('click', () => {
        eventModal.close();
        // if where editing an appointment, reset the form
        if (appointmentEditor.event_id.value) {
            setAppointmentDataInEditor();
        }
    });

    // appointmentEditor.addEventListener('submit', handleAppointmentSubmission);

    const endDateInput = appointmentEditor.querySelector('#endDatetime');
    const startDateInput = appointmentEditor.querySelector('#startDatetime');        

    endDateInput.addEventListener('change', (event) => { adjustTimeToNearestInterval(event, calendar_config.appointment_duration); });

    // whenever the start date changes, update the end date to be the start date + appointment duration
    startDateInput.addEventListener('change', (event) => {
        adjustTimeToNearestInterval(event, calendar_config.appointment_duration);
        
        const startDate = new Date(event.target.value);
        
        const endDate = addMinutesToDate(startDate, calendar_config.appointment_duration * 60 - 1);
        
        // Format endDate to local date-time string
        const year = endDate.getFullYear();
        const month = String(endDate.getMonth() + 1).padStart(2, '0');
        const day = String(endDate.getDate()).padStart(2, '0');
        const hours = String(endDate.getHours()).padStart(2, '0');
        const minutes = String(endDate.getMinutes()).padStart(2, '0');
        
        endDateInput.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    });


}

function addEventListeners() {
    prevDaysBtn.addEventListener('click', () => {
        updateCalendar(-1);
    });

    nextDaysBtn.addEventListener('click', () => {
        updateCalendar(1);
    });

    todayBtn.addEventListener('click', () => {
        // calcula la diferencia de dias entre la fecha actual y la fecha en el calendario
        /*
        const dataOnCalendar = {
            day: currentDay,
            month: currentMonth,
            year: currentYear,
            dayOfWeek: currentDayOfWeek
        };
        */
        const currentDate = new Date();
        const currentDay = currentDate.getDate();
        const currentMonth = currentDate.getMonth();
        const currentYear = currentDate.getFullYear();
        const currentDayOfWeek = currentDate.getDay();
        const newDate = {
            day: currentDay,
            month: currentMonth,
            year: currentYear,
            dayOfWeek: currentDayOfWeek
        };
        const diffDays = (new Date(newDate.year, newDate.month, newDate.day) - new Date(dataOnCalendar.year, dataOnCalendar.month, dataOnCalendar.day)) / (1000 * 60 * 60 * 24);
        updateCalendar(diffDays);
        
    });
    addModalEventListeners();
}

function setAppointmentDataInEditor(appointmentData) {
    
    if (appointmentData) {
        document.querySelector("#modalTitle").textContent = 'Editar Cita';
        // fill the form
        appointmentEditor.event_id.value = appointmentData.id;
        appointmentEditor.full_name.value = appointmentData.full_name;
        appointmentEditor.email.value = appointmentData.email;
        appointmentEditor.phone_number.value = appointmentData.phone_number;
        appointmentEditor.message.value = appointmentData.message;

        // Convert start_datetime and end_datetime to local datetime format
        const startDate = new Date(appointmentData.start_datetime);
        const endDate = new Date(appointmentData.end_datetime);

        const startDateTimeLocal = new Date(startDate.getTime() - startDate.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
        const endDateTimeLocal = new Date(endDate.getTime() - endDate.getTimezoneOffset() * 60000).toISOString().slice(0, 16);

        appointmentEditor.start_datetime.value = startDateTimeLocal;
        appointmentEditor.end_datetime.value = endDateTimeLocal;

        // get the #deleteEventBtn and show it
        deleteEventBtn.classList.remove('hidden');
        deleteEventBtn.addEventListener('click', async () => {
            const response = await myFetch(`cancel-appointment/${appointmentData.cancel_token}/`, {
                message: prompt('Por favor, ingrese un mensaje que verá el usuario:')
            }, 'DELETE');
            if (response.status === 'success') {
                showAlert('success', '¡Cita eliminada exitosamente!');
                eventModal.close();
                setTimeout(() => { window.location.reload(); }, 1000);
            } else {
                showAlert('error', `Error: ${response.message}`);
            }
        })

    }else {
        document.querySelector("#modalTitle").textContent = 'Nueva Cita';
        appointmentEditor.reset();
        appointmentEditor.event_id.value = null;

        // get the #deleteEventBtn and hidde it
        deleteEventBtn.classList.add('hidden');
    }
}

function scrollToCurrentHour() {
    const idealHourToScroll = Math.max(currentHour - 2, 0)
    const hourToScroll =  idealHourToScroll < calendar_config.appointment_start_time  ? calendar_config.appointment_start_time : 
                        idealHourToScroll > calendar_config.appointment_end_time ? calendar_config.appointment_end_time : idealHourToScroll;
    
    window[`day1Hour${hourToScroll}`].scrollIntoView({ behavior: 'smooth', block: 'start' });
}
// Initialize
main();