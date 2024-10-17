// Constants
const DAYS_OF_WEEK = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
const MONTHS_OF_YEAR = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

// Elements
const calendar_config = JSON.parse(document.getElementById('calendar_config').textContent);
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
// console.log(appointments);


const calendar = document.querySelector('#calendar');
const headerDay1 = document.querySelector('#headerDay1');
const headerDay2 = document.querySelector('#headerDay2');
const headerDay3 = document.querySelector('#headerDay3');
const headers = [headerDay1, headerDay2, headerDay3];
const prevDaysBtn = document.getElementById('prevDaysBtn');
const nextDaysBtn = document.getElementById('nextDaysBtn');

// Modal Elements
const addEventBtn = document.getElementById('addEventBtn');
const eventModal = document.getElementById('eventModal');
const closeModalBtn = document.getElementById('closeModalBtn');

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
    addModalEventListeners();
}

function syncMiniBoxesToHours() {
    const hourBoxes = document.querySelectorAll('.hourBox');
    const durationInMinutes = calendar_config.appointment_duration * 60;
    const amountOfMiniBoxes = Math.floor(1 / calendar_config.appointment_duration);
    const template = document.getElementById('miniHourBox').content;
    const template2 = document.getElementById('miniHourBoxBusy').content;

    hourBoxes.forEach((hourBox) => {
        hourBox.innerHTML = ""; // clear the hourBox
        for (let i = 0; i < amountOfMiniBoxes; i++) {
            const hour = parseInt(hourBox.id.split('Hour')[1]);
            const dayIndex = parseInt(hourBox.id.split('Hour')[0].split('day')[1])-1;
            const day = parseInt(headers[dayIndex].querySelector('.day').textContent);

            const miniBoxData = {
                hour: hour,
                hourIndex: i,
                day: day,
                month: dataOnCalendar.month,
                year: dataOnCalendar.year,
                startMinute: hour * 60,
                endMinute: hour * 60 + durationInMinutes 
            };
            const boxPseudoId = `${miniBoxData.year}-${String(miniBoxData.month + 1).padStart(2, '0')}-${String(miniBoxData.day).padStart(2, '0')}-${miniBoxData.startMinute}-${miniBoxData.endMinute}`;

            
            // check if the hour is in the appointments
            const existingAppointment = appointments.find(appointment => {
                const [year, month, day] = appointment.pseudoId.split('-');
                const [boxYear, boxMonth, boxDay] = boxPseudoId.split('-');
                return year === boxYear && month === boxMonth && day === boxDay;
            });
            const appointmentExits = () => {
                // if the appointment contains the hour
                if (existingAppointment) {
                    const start = existingAppointment.start_datetime.getUTCHours() * 60 + existingAppointment.start_datetime.getMinutes();
                    const end = existingAppointment.end_datetime.getUTCHours() * 60 + existingAppointment.end_datetime.getMinutes();
                    return start <= miniBoxData.startMinute && end >= miniBoxData.endMinute;
                }
            }
            

            // Clonar el contenido del template
            const miniBox = document.importNode(!!appointmentExits()? template2 : template, true).firstElementChild;
            

            // Modificar el contenido clonado
            
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

function addDays(days = 1, data = dataOnCalendar) {
    const date = new Date(data.year, data.month, data.day);
    date.setDate(date.getDate() + days);

    return {
        day: date.getDate(),
        month: date.getMonth(),
        year: date.getFullYear(),
        dayOfWeek: date.getDay()
    };
}

function subtractDays(days = 1, data = dataOnCalendar) {
    return addDays(-days, data);
}

function addEventListeners() {
    prevDaysBtn.addEventListener('click', () => {
        updateCalendar(-1);
    });

    nextDaysBtn.addEventListener('click', () => {
        updateCalendar(1);
    });
}

function updateCalendar(days) {
    const newDate = days > 0 ? addDays(days) : subtractDays(-days);
    Object.assign(dataOnCalendar, newDate);
    syncDataOnCalendar(dataOnCalendar);
}

function addModalEventListeners() {
    addEventBtn.addEventListener('click', () => {
        eventModal.showModal();
    });

    closeModalBtn.addEventListener('click', () => {
        eventModal.close();
    });
}

// Initialize
main();