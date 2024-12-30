document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.querySelector('.carousel');
    const dots = document.querySelectorAll('.dot');
    const items = document.querySelectorAll('.carousel-item');
    let currentIndex = 0;

    // Function to update carousel position and active dot
    function updateCarousel(index) {
        const offset = -index * 100; // Shift the carousel by 100% for each index
        carousel.style.transform = `translateX(${offset}%)`;

        // Update active dot
        dots.forEach(dot => dot.classList.remove('active'));
        dots[index].classList.add('active');
    }

    // Event listeners for dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentIndex = index;
            updateCarousel(currentIndex);
        });
    });

    // Auto-rotation logic
    setInterval(() => {
        currentIndex = (currentIndex + 1) % items.length; // Loop back to the start
        updateCarousel(currentIndex);
    }, 5000); // Adjust rotation speed in milliseconds

    // Initialize carousel
    updateCarousel(currentIndex);
});
