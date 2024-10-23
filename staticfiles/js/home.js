const sliderContainer = document.getElementById('slider-container');
const pagination = document.getElementById('pagination');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let currentIndex = 0;
const totalSlides = sliderContainer.children.length;

const updateSlider = () => {
    sliderContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    Array.from(pagination.children).forEach((indicator, index) => {
        indicator.classList.toggle('bg-opacity-100', index === currentIndex);
        indicator.classList.toggle('bg-opacity-50', index !== currentIndex);
    });
};

const goToSlide = index => {
    currentIndex = index;
    updateSlider();
};

const nextSlide = () => {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateSlider();
};

const prevSlide = () => {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateSlider();
};

prevBtn.addEventListener('click', prevSlide);
nextBtn.addEventListener('click', nextSlide);

Array.from(pagination.children).forEach((indicator, index) => {
    indicator.addEventListener('click', () => goToSlide(index));
});

// Auto-sliding
// setInterval(nextSlide, 5000);
