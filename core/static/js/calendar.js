import { myFetch, showAlert, DAYS_OF_WEEK, MONTHS_OF_YEAR, addDays, subtractDays, adjustTimeToNearestInterval, addMinutesToDate } from "./helpers.js";

// Elements
const calendar_config = JSON.parse(document.getElementById('calendar_config').textContent);

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

const calendar = document.querySelector('#calendar');
const headerDay1 = document.querySelector('#headerDay1');
const headerDay2 = document.querySelector('#headerDay2');
const headerDay3 = document.querySelector('#headerDay3');
const headers = [headerDay1, headerDay2, headerDay3];
const prevDaysBtn = document.getElementById('prevDaysBtn');
const nextDaysBtn = document.getElementById('nextDaysBtn');

// Modal Elements
const eventModal = document.querySelector('#eventModal');
const appointmentEditor = eventModal.querySelector('#appointmentEditor');

const addEventBtn = document.querySelector('#addEventBtn');
const closeModalBtn = appointmentEditor.querySelector('#closeModalBtn');

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
    window[`day1Hour${Math.max(currentHour - 2, 0)}`].scrollIntoView({ behavior: 'smooth', block: 'start' }); // scrollToCurrentHour

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
            const endMinute = startMinute + durationInMinutes;
    
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
    
            const existingAppointment = appointments.find(appointment => 
                appointment.start_datetime.getDate() === miniBoxData.day &&
                appointment.start_datetime.getUTCHours() * 60 + appointment.start_datetime.getMinutes() < miniBoxData.endMinute &&
                appointment.end_datetime.getUTCHours() * 60 + appointment.end_datetime.getMinutes() > miniBoxData.startMinute
            );
    
            let miniBox;
            if (isOffTime || isOffDay) {
                miniBox = document.importNode(templateOff, true).firstElementChild;
            } else if (existingAppointment) {
                miniBox = document.importNode(templateBusy, true).firstElementChild;
                
                miniBox.addEventListener('click', () => { 
                    setAppointmentDataInEditor(existingAppointment); 
                    eventModal.show(); 
                });
            } else {
                miniBox = document.importNode(template, true).firstElementChild;
                // when clicked, set the start and end time in the form
                miniBox.addEventListener('click', () => {
                    const startDate = new Date(dataOnCalendar.year, dataOnCalendar.month, day, hour, i * calendar_config.appointment_duration);
                    const endDate = addMinutesToDate(startDate, calendar_config.appointment_duration * 60);
                
                    // Convertir a naive eliminando la información de la zona horaria
                    const naiveStartDate = new Date(startDate.getTime() - (startDate.getTimezoneOffset() * 60000));
                    const naiveEndDate = new Date(endDate.getTime() - (endDate.getTimezoneOffset() * 60000));
                
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

const handleAppointmentSubmission = async (event) => {
    event.preventDefault();
    const appointmentForm = event.target;

    const formData = new FormData(appointmentForm);
    const data = Object.fromEntries(formData.entries());

    // Verificar que todos los campos requeridos estén completos
    if (!data.full_name || !data.start_datetime || !data.end_datetime) {
        showAlert('error', 'Por favor, complete todos los campos requeridos.');
        return;
    }

    try {
        const method = data.event_id ? 'PUT' : 'POST';
        const response = await myFetch('create-appointment/', data, method);
        if (response.status === 'success') {
            showAlert('success', `¡Cita ${method === 'POST' ? 'creada' : 'actualizada'} exitosamente!`);
            appointmentForm.reset(); // Limpiar el formulario después de la creación/actualización exitosa
            eventModal.close();
            setTimeout(() => { window.location.reload();}, 1000);
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

    appointmentEditor.addEventListener('submit', handleAppointmentSubmission);

    const endDateInput = appointmentEditor.querySelector('#endDatetime');
    const startDateInput = appointmentEditor.querySelector('#startDatetime');        

    endDateInput.addEventListener('change', (event) => { adjustTimeToNearestInterval(event, calendar_config.appointment_duration); });

    // whenever the start date changes, update the end date to be the start date + appointment duration
    startDateInput.addEventListener('change', (event) => {
        adjustTimeToNearestInterval(event, calendar_config.appointment_duration);
        
        const startDate = new Date(event.target.value);
        
        const endDate = addMinutesToDate(startDate, calendar_config.appointment_duration * 60);
        
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
        appointmentEditor.start_datetime.value = appointmentData.start_datetime.toISOString().slice(0, 16);
        appointmentEditor.end_datetime.value = appointmentData.end_datetime.toISOString().slice(0, 16);
        
    } else {
        document.querySelector("#modalTitle").textContent = 'Nueva Cita';
        appointmentEditor.reset();
        appointmentEditor.event_id.value = null;
    }
}

// Initialize
main();