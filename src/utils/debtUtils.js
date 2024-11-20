// Function to update the debt counter value and display
export function updateCounter(value) {
    const incrementDuration = 1000;
    const startValue = counterValue;
    const endValue = counterValue + value;
    const startTime = performance.now();

    function animateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / incrementDuration, 1); // Cap at 1 (100%)

        // Interpolate the counter value
        const currentDisplayValue = Math.round(startValue + (endValue - startValue) * progress);

        // Update the counter text
        counterText.text = `Debt Owed: ${currentDisplayValue}`;

        // Continue animating if not yet complete
        if (progress < 1) {
            requestAnimationFrame(animateCounter);
        } else {
            // Finalize the counter value
            counterValue = endValue;
        }
    }

    requestAnimationFrame(animateCounter);
}