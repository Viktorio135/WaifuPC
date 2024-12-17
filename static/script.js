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

    let currentIndex = 0; // Текущий индекс
    let startX = 0; // Координата начала свайпа
    let isDragging = false; // Флаг свайпа
    let currentTranslate = 0; // Текущее смещение
    let prevTranslate = 0; // Предыдущее смещение

    function getSlidesPerView() {
        const width = window.innerWidth;
        if (width <= 480) return 1; // Одна карточка на маленьких экранах
        if (width <= 768) return 2; // Две карточки на средних экранах
        return 3; // Три карточки на больших экранах
    }

    function setSliderPosition() {
        slider.style.transform = `translateX(${currentTranslate}px)`;
    }

    function updateSlider() {
        const slidesPerView = getSlidesPerView();
        const slideWidth = slider.offsetWidth / slidesPerView; // Рассчитываем ширину одной карточки
        currentTranslate = -currentIndex * slideWidth;
        prevTranslate = currentTranslate; // Сохраняем позицию
        setSliderPosition();

        // Обновляем кнопки
        prevButton.classList.toggle('inactive', currentIndex === 0);
        nextButton.classList.toggle(
            'inactive',
            currentIndex >= slides.length - slidesPerView
        );
    }

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateSlider();
        }
    });

    nextButton.addEventListener('click', () => {
        const slidesPerView = getSlidesPerView();
        if (currentIndex < slides.length - slidesPerView) {
            currentIndex++;
            updateSlider();
        }
    });

    // Обработка свайпов
    slider.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
        slider.style.transition = 'none'; // Отключаем анимацию во время свайпа
    });

    slider.addEventListener('touchmove', (e) => {
        if (!isDragging) return;

        const currentX = e.touches[0].clientX;
        const deltaX = currentX - startX; // Сдвиг пальца
        currentTranslate = prevTranslate + deltaX; // Расчет текущего смещения
        setSliderPosition(); // Обновление позиции слайдера
    });

    slider.addEventListener('touchend', () => {
        if (!isDragging) return;

        isDragging = false;
        const slidesPerView = getSlidesPerView();
        const slideWidth = slider.offsetWidth / slidesPerView; // Рассчитываем ширину карточки
        const movedBy = currentTranslate - prevTranslate; // Общее смещение за свайп

        // Если свайп больше половины ширины карточки, переходим к следующему или предыдущему
        if (movedBy < -slideWidth / 2 && currentIndex < slides.length - slidesPerView) {
            currentIndex++;
        } else if (movedBy > slideWidth / 2 && currentIndex > 0) {
            currentIndex--;
        }

        updateSlider(); // Возвращаем позицию слайдера
        slider.style.transition = 'transform 0.3s ease'; // Возвращаем анимацию
    });

    // Обновляем слайдер при изменении размера экрана
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