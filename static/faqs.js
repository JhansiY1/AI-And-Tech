document.addEventListener("DOMContentLoaded", () => {
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        const question = item.querySelector(".question");

        question.addEventListener("click", () => {
            const answer = item.querySelector(".answer");

            if (answer.style.display === "block") {
                answer.style.display = "none";
            } else {
                // Close any open answers
                faqItems.forEach(i => {
                    i.querySelector(".answer").style.display = "none";
                });

                // Open the clicked answer
                answer.style.display = "block";
            }
        });
    });
});
