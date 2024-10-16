// Constants
const DAYS_OF_WEEK = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
const MONTHS_OF_YEAR = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

// Elements
const calendarConfig = JSON.parse(document.getElementById('calendar_config').textContent);
const calendar = document.querySelector('#calendar');
const headerDay1 = document.querySelector('#headerDay1');
const headerDay2 = document.querySelector('#headerDay2');
const headerDay3 = document.querySelector('#headerDay3');
const headers = [headerDay1, headerDay2, headerDay3];
const prevDaysBtn = document.getElementById('prevDaysBtn');
const nextDaysBtn = document.getElementById('nextDaysBtn');

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

// Functions
function initializeCalendar() {
    window[`day1Hour${Math.max(currentHour - 2, 0)}`].scrollIntoView({ behavior: 'smooth', block: 'start' }); // scrollToCurrentHour
    syncDataOnCalendar(dataOnCalendar);
    addEventListeners();
}

    

function syncDataOnCalendar(givenData = dataOnCalendar) {
    headers.forEach((header, index) => {
        const dayElement = header.querySelector('.day');
        const weekDayElement = header.querySelector('.weekDay');
        const newDate = addDays(index, givenData);

        updateHeaderStyles(dayElement, weekDayElement, newDate);
        updateHeaderContent(dayElement, weekDayElement, newDate);
    });

    
    // update the month and year
    window.month.textContent = MONTHS_OF_YEAR[givenData.month];
    window.year.textContent = givenData.year;
}

function updateHeaderStyles(dayElement, weekDayElement, newDate) {
    if (isCurrentDate(newDate)) {
        dayElement.classList.add('secondary-light-bg');
        weekDayElement.classList.add('primary-dark-color');
    } else {
        dayElement.classList.remove('secondary-light-bg');
        weekDayElement.classList.remove('primary-dark-color');
    }
}

function updateHeaderContent(dayElement, weekDayElement, newDate) {
    dayElement.textContent = newDate.day;
    weekDayElement.textContent = getDayName(newDate.dayOfWeek);
}

function isCurrentDate(date) {
    return date.day === currentDay && date.month === currentMonth && date.year === currentYear;
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

function getDayName(dayOfWeek) {
    return DAYS_OF_WEEK[dayOfWeek];
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

// Initialize
initializeCalendar();