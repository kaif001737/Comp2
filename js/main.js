/**
 * St. Antony's Girls Higher Secondary School - Client-Side Interactive Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- Sticky Header & Scroll Effects ---
    const header = document.querySelector('header');
    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Run initially to set state if page is refreshed down

    // --- Mobile Menu Toggle ---
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    const navOverlay = document.getElementById('navOverlay');

    const setMobileMenuState = (isOpen) => {
        if (!navMenu || !mobileBtn) return;
        navMenu.classList.toggle('active', isOpen);
        document.body.classList.toggle('nav-open', isOpen);
        mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        if (navOverlay) {
            navOverlay.classList.toggle('active', isOpen);
            navOverlay.hidden = !isOpen;
        }
        const icon = mobileBtn.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-bars', !isOpen);
            icon.classList.toggle('fa-times', isOpen);
        }
    };

    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            setMobileMenuState(!navMenu.classList.contains('active'));
        });

        if (navOverlay) {
            navOverlay.addEventListener('click', () => setMobileMenuState(false));
        }

        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => setMobileMenuState(false));
        });

        document.addEventListener('click', (e) => {
            if (!navMenu.classList.contains('active')) return;
            if (!navMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                setMobileMenuState(false);
            }
        });
    }

    // --- Scroll-Triggered Animations ---
    const animatedElements = document.querySelectorAll('.fade-in, .slide-up');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('appear');
                    observer.unobserve(entry.target); // Stop observing once it has animated
                }
            });
        }, {
            threshold: 0.15,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(el => observer.observe(el));
    } else {
        // Fallback for older browsers
        animatedElements.forEach(el => el.classList.add('appear'));
    }

    // --- Hero Slider / Carousel ---
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    if (slides.length > 0) {
        let currentSlide = 0;
        let slideInterval;

        const showSlide = (index) => {
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            slides[index].classList.add('active');
            dots[index].classList.add('active');
            currentSlide = index;
        };

        const nextSlide = () => {
            let next = (currentSlide + 1) % slides.length;
            showSlide(next);
        };

        const startSlideShow = () => {
            slideInterval = setInterval(nextSlide, 6000);
        };

        const resetSlideShow = () => {
            clearInterval(slideInterval);
            startSlideShow();
        };

        // Add click events to dots
        dots.forEach((dot, idx) => {
            dot.addEventListener('click', () => {
                showSlide(idx);
                resetSlideShow();
            });
        });

        // Initialize slideshow
        showSlide(0);
        startSlideShow();
    }

    // --- Accordions (Admissions Page) ---
    const accordions = document.querySelectorAll('.accordion-header');
    accordions.forEach(acc => {
        acc.addEventListener('click', function() {
            const item = this.parentElement;
            const isActive = item.classList.contains('active');
            
            // Close all items
            document.querySelectorAll('.accordion-item').forEach(el => {
                el.classList.remove('active');
            });
            
            // Toggle clicked item
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // --- Gallery Filter Logic ---
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    if (filterButtons.length > 0 && galleryItems.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                // Set active button style
                filterButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filterValue = this.getAttribute('data-filter');
                
                galleryItems.forEach(item => {
                    const categories = item.getAttribute('data-category').split(' ');
                    if (filterValue === 'all' || categories.includes(filterValue)) {
                        item.classList.remove('hide');
                        // Small animation delay for appearance
                        item.style.opacity = '0';
                        setTimeout(() => {
                            item.style.opacity = '1';
                        }, 50);
                    } else {
                        item.classList.add('hide');
                    }
                });
            });
        });
    }

    // --- Gallery Lightbox Modal ---
    const galleryGridItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('galleryLightbox');
    const lightboxImg = lightbox ? lightbox.querySelector('.lightbox-img') : null;
    const lightboxCaption = lightbox ? lightbox.querySelector('.lightbox-caption') : null;
    const lightboxClose = lightbox ? lightbox.querySelector('.lightbox-close') : null;

    if (galleryGridItems.length > 0 && lightbox && lightboxImg) {
        galleryGridItems.forEach(item => {
            item.addEventListener('click', () => {
                const img = item.querySelector('.gallery-item-img');
                const title = item.querySelector('.gallery-item-title').textContent;
                
                if (img) {
                    lightboxImg.src = img.src;
                    lightboxImg.alt = img.alt;
                    lightboxCaption.textContent = title;
                    lightbox.classList.add('active');
                    document.body.style.overflow = 'hidden'; // Lock background scrolling
                }
            });
        });

        // Close functions
        const closeLightbox = () => {
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
            setTimeout(() => {
                lightboxImg.src = '';
            }, 300); // Clear image source after transition finishes
        };

        lightboxClose.addEventListener('click', closeLightbox);
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('active')) {
                closeLightbox();
            }
        });
    }

    // --- AJX Forms (Admissions inquiry & Contact forms) ---
    const inquiryForm = document.getElementById('admissionInquiryForm');
    if (inquiryForm) {
        inquiryForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const feedback = document.getElementById('formFeedback');
            
            // Set Loading state
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            
            // Hide previous feedback
            feedback.style.display = 'none';
            feedback.className = 'form-feedback';
            
            // Get form values
            const formData = {
                studentName: document.getElementById('studentName').value.trim(),
                parentName: document.getElementById('parentName').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                grade: document.getElementById('grade').value,
                message: document.getElementById('message').value.trim()
            };
            
            try {
                const response = await fetch('/submit-inquiry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    feedback.classList.add('success');
                    feedback.textContent = result.message;
                    feedback.style.display = 'block';
                    this.reset(); // Reset form fields
                } else {
                    feedback.classList.add('error');
                    feedback.textContent = result.message || 'Verification failed. Please check inputs.';
                    feedback.style.display = 'block';
                }
            } catch (error) {
                feedback.classList.add('error');
                feedback.textContent = 'Server communication error. Please try again later.';
                feedback.style.display = 'block';
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                
                // Scroll to feedback message
                feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    }

    const contactForm = document.getElementById('schoolContactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const feedback = document.getElementById('contactFeedback');
            
            // Set Loading state
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            
            // Hide previous feedback
            feedback.style.display = 'none';
            feedback.className = 'form-feedback';
            
            // Get form values
            const formData = {
                name: document.getElementById('contactName').value.trim(),
                email: document.getElementById('contactEmail').value.trim(),
                subject: document.getElementById('contactSubject').value.trim(),
                message: document.getElementById('contactMessage').value.trim()
            };
            
            try {
                const response = await fetch('/submit-contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    feedback.classList.add('success');
                    feedback.textContent = result.message;
                    feedback.style.display = 'block';
                    this.reset(); // Reset form fields
                } else {
                    feedback.classList.add('error');
                    feedback.textContent = result.message || 'Verification failed. Please check inputs.';
                    feedback.style.display = 'block';
                }
            } catch (error) {
                feedback.classList.add('error');
                feedback.textContent = 'Server communication error. Please try again later.';
                feedback.style.display = 'block';
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                
                // Scroll to feedback message
                feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    }
});
