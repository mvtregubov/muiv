(function () {
    const form = document.getElementById('quiz-form');
    const timerElement = document.getElementById('timer');

    if (!form || !timerElement) {
        return;
    }

    const duration = parseInt(timerElement.dataset.minutes || '15', 10) * 60;
    let remaining = duration;

    const renderTime = () => {
        const minutes = Math.floor(remaining / 60);
        const seconds = remaining % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    };

    renderTime();

    const interval = window.setInterval(() => {
        remaining -= 1;
        renderTime();
        if (remaining <= 0) {
            window.clearInterval(interval);
            form.submit();
        }
    }, 1000);
})();
