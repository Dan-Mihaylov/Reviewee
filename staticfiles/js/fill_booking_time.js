document.addEventListener('DOMContentLoaded', function() {
    const bookingDateInput = document.getElementById('id_date');
    const bookingTimeSelect = document.getElementById('id_booking_time');

    function addTimeOptions(startHour, endHour, interval) {
        bookingTimeSelect.innerHTML = '';
        for (let hour = startHour; hour <= endHour; hour++) {
            for (let minute = 0; minute < 60; minute += interval) {
                const hourPadded = hour < 10 ? '0' + hour : hour;
                const minutePadded = minute < 10 ? '0' + minute : minute;
                const timeValue = `${hourPadded}:${minutePadded}:00`;
                const timeDisplay = `${hourPadded}:${minutePadded}`;
                const option = new Option(timeDisplay, timeValue);
                bookingTimeSelect.add(option);
            }
        }
    }

    bookingDateInput.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);

        if (selectedDate.toDateString() === currentDate.toDateString()) {
            const currentHour = new Date().getHours();
            const openingHour = parseInt(restaurantTimes.opening_time.split(':')[0]);
            const startHour = Math.max(currentHour, openingHour);
            addTimeOptions(startHour, 23, 30);
        } else {
            const openingHour = parseInt(restaurantTimes.opening_time.split(':')[0]);
            const closingHour = parseInt(restaurantTimes.closing_time.split(':')[0]);
            addTimeOptions(openingHour, closingHour, 30);
        }
    });
});
