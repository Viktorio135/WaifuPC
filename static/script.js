document.addEventListener("DOMContentLoaded", function() {
    // Анимация секций
    const sections = document.querySelectorAll('.section');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
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

    // Управляем видимостью кнопок
    prevButton.classList.toggle('visible', currentIndex > 0);
    nextButton.classList.toggle('visible', currentIndex < slides.length - slidesPerView);
    }

    prevButton.addEventListener('click', () => {
    currentIndex--;
    updateSlider();
    });

    nextButton.addEventListener('click', () => {
    currentIndex++;
    updateSlider();
    });

    // Обновляем слайдер и кнопки при изменении размера экрана
    window.addEventListener('resize', updateSlider);

    // Инициализация
    updateSlider();


    


});