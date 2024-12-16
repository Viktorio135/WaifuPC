document.addEventListener("DOMContentLoaded", function() {
    // Анимация секций
    const animationKey = 'sectionsAnimated';
    const sections = document.querySelectorAll('.section');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('visible')) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    sections.forEach(section => {
        observer.observe(section);
    });

    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');

    let currentIndex = 0;

    function getSlidesPerView() {
        const width = window.innerWidth;
        if (width <= 480) return 1; // Одна карточка на очень маленьком экране
        if (width <= 768) return 2; // Две карточки на небольшом экране
        return 3; // Три карточки на больших экранах
    }

    function updateSlider() {
        const slidesPerView = getSlidesPerView();
        const offset = -(currentIndex * (100 / slidesPerView));
        slider.style.transform = `translateX(${offset}%)`;

        // Управляем активностью кнопок
        if (currentIndex === 0) {
            prevButton.classList.add('inactive');
        } else {
            prevButton.classList.remove('inactive');
        }

        if (currentIndex >= slides.length - slidesPerView) {
            nextButton.classList.add('inactive');
        } else {
            nextButton.classList.remove('inactive');
        }
    }

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) { // Проверяем, можно ли листать назад
            currentIndex--;
            updateSlider();
        }
    });

    nextButton.addEventListener('click', () => {
        const slidesPerView = getSlidesPerView();
        if (currentIndex < slides.length - slidesPerView) { // Проверяем, можно ли листать вперед
            currentIndex++;
            updateSlider();
        }
    });

    // Обновляем слайдер и кнопки при изменении размера экрана
    window.addEventListener('resize', updateSlider);

    // Инициализация
    updateSlider();

    const notification = document.querySelector(".notification");
    const closeButton = document.querySelector(".notification-close");

    if (notification) {
        notification.classList.add("active");

        closeButton.addEventListener("click", () => {
            notification.classList.remove("active");
        });

        setTimeout(() => {
            notification.classList.remove("active");
        }, 7500);
    }


});