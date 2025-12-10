document.addEventListener('DOMContentLoaded', () => {
    // --- Language Switching ---
    const langButtons = document.querySelectorAll('.lang-btn');
    const instagramLink = document.getElementById('instagram-link');
    
    // Check localStorage or default to 'ru'
    let currentLang = localStorage.getItem('siteLanguage') || 'ru';
    setLanguage(currentLang);

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.getAttribute('data-lang');
            setLanguage(lang);
        });
    });

    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('siteLanguage', lang);
        document.documentElement.lang = lang;

        // Update active button state
        langButtons.forEach(btn => {
            if (btn.getAttribute('data-lang') === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update text content
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                if (key === 'hero_title') {
                    element.innerHTML = translations[lang][key];
                } else {
                    element.textContent = translations[lang][key];
                }
            }
        });

        // Update Instagram Link
        if (translations[lang] && translations[lang].instagram_url) {
            if (instagramLink) {
                instagramLink.href = translations[lang].instagram_url;
            }
        }

        // Update Quiz Links
        const quizLinks = document.querySelectorAll('a[href^="quiz.html"]');
        quizLinks.forEach(link => {
            link.href = `quiz.html?lang=${lang}`;
        });

        // Update Carousel Text
        updateCarouselText(lang);
    }

    function updateCarouselText(lang) {
        document.querySelectorAll('.carousel-caption').forEach(caption => {
            const id = caption.getAttribute('data-id');
            if (id && translations[lang]) {
                const title = translations[lang][`p_${id}_title`];
                const desc = translations[lang][`p_${id}_desc`];
                if (title) caption.querySelector('h3').textContent = title;
                if (desc) caption.querySelector('p').textContent = desc;
            }
        });
    }

    // --- Mobile Menu ---
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });
    }

    // --- Carousel ---
    const track = document.querySelector('.carousel-track');
    const nextButton = document.querySelector('.carousel-btn.next');
    const prevButton = document.querySelector('.carousel-btn.prev');
    
    // Image list with IDs
    const paintings = [
        { id: 1, src: '1.jpg' }, { id: 2, src: '2.jpg' }, { id: 3, src: '3.jpg' }, { id: 4, src: '4.jpg' },
        { id: 5, src: '5.jpg' }, { id: 6, src: '6.jpg' }, { id: 7, src: '7.jpg' }, { id: 8, src: '8.jpg' },
        { id: 9, src: '9.jpg' }, { id: 10, src: '10.jpg' }, { id: 11, src: '11.jpg' }, { id: 12, src: '12.jpg' },
        { id: 13, src: '13.jpg' }, { id: 14, src: '14.jpg' }, { id: 15, src: '15.jpg' }, { id: 16, src: '16.jpg' }
    ];

    if (track && paintings.length > 0) {
        // Populate carousel
        paintings.forEach(p => {
            const li = document.createElement('li');
            li.classList.add('carousel-slide');
            
            const img = document.createElement('img');
            img.src = `assets/paintings/${p.src}`;
            img.alt = `Painting ${p.id}`;
            img.loading = 'lazy';
            
            const caption = document.createElement('div');
            caption.classList.add('carousel-caption');
            caption.setAttribute('data-id', p.id);
            
            const h3 = document.createElement('h3');
            const desc = document.createElement('p');
            
            caption.appendChild(h3);
            caption.appendChild(desc);
            
            li.appendChild(img);
            li.appendChild(caption);
            track.appendChild(li);
        });

        // Initial text update
        updateCarouselText(currentLang);

        const slides = Array.from(track.children);
        let currentIndex = 0;

        function updateCarousel() {
            if (slides.length === 0) return;
            
            // Calculate items per view based on CSS
            const containerWidth = track.parentElement.getBoundingClientRect().width;
            const slideWidth = slides[0].getBoundingClientRect().width;
            const itemsPerView = Math.round(containerWidth / slideWidth);
            
            // Limit index
            const maxIndex = slides.length - itemsPerView;
            if (currentIndex > maxIndex) currentIndex = maxIndex;
            if (currentIndex < 0) currentIndex = 0;

            track.style.transform = 'translateX(-' + (slideWidth * currentIndex) + 'px)';
        }

        window.addEventListener('resize', updateCarousel);

        if (nextButton) {
            nextButton.addEventListener('click', () => {
                const containerWidth = track.parentElement.getBoundingClientRect().width;
                const slideWidth = slides[0].getBoundingClientRect().width;
                const itemsPerView = Math.round(containerWidth / slideWidth);
                
                if (currentIndex < slides.length - itemsPerView) {
                    currentIndex++;
                } else {
                    currentIndex = 0; // Loop back to start
                }
                updateCarousel();
            });
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                const containerWidth = track.parentElement.getBoundingClientRect().width;
                const slideWidth = slides[0].getBoundingClientRect().width;
                const itemsPerView = Math.round(containerWidth / slideWidth);

                if (currentIndex > 0) {
                    currentIndex--;
                } else {
                    currentIndex = slides.length - itemsPerView; // Loop to end
                }
                updateCarousel();
            });
        }
        
        setTimeout(updateCarousel, 100);
    }
    
    // --- Fade In Animation ---
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in, .section').forEach(section => {
        section.classList.add('fade-in-hidden');
        observer.observe(section);
    });
});
