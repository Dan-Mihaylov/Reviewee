function updateNotificationCount() {
    let notificationBellP = document.getElementById('notification-bell-p');
    let apiUrl = "/api/unread-notifications-count/"
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.unread_count > 0){
            notificationBellP.textContent = data.unread_count;
            } else {
                notificationBellP.textContent = null;
            }
        })
        .catch(error => {
            console.error('Error fetching unread notifications', error);
        });
}

document.addEventListener('DOMContentLoaded', updateNotificationCount);
