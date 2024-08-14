function startCountdown(id) {
    let countdownDate;
    countdownDate = new Date(document.getElementById(`limited_offers_${id}`).innerText).getTime();

    countdown = document.getElementById(`countdown_${id}`);

    let x = setInterval(function() {
        let now = new Date().getTime();
        
        let distance = countdownDate - now;
        
        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        countdown.querySelector("#days").innerHTML = days.toString().padStart(2, '0');
        countdown.querySelector("#hours").innerHTML = hours.toString().padStart(2, '0');
        countdown.querySelector("#minutes").innerHTML = minutes.toString().padStart(2, '0');
        countdown.querySelector("#seconds").innerHTML = seconds.toString().padStart(2, '0');

        if (distance >= 0) {
            countdown.style.display = "flex";
            return;
        } else {
            clearInterval(x);
        }
    }, 1000);
};