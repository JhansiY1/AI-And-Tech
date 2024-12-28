document.addEventListener("DOMContentLoaded", function() {
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");
  const carousel = document.querySelector(".carousel");
  const images = document.querySelectorAll(".carousel img");

  let currentIndex = 0;

  function updateCarousel() {
      const width = images[0].clientWidth;
      carousel.style.transform = `translateX(-${currentIndex * width}px)`;
  }

  nextButton.addEventListener("click", function() {
      if (currentIndex < images.length - 1) {
          currentIndex++;
      } else {
          currentIndex = 0;  // Loop back to the first image
      }
      updateCarousel();
  });

  prevButton.addEventListener("click", function() {
      if (currentIndex > 0) {
          currentIndex--;
      } else {
          currentIndex = images.length - 1;  // Loop back to the last image
      }
      updateCarousel();
  });

  // Initial carousel setup
  updateCarousel();
});
