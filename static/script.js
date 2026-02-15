
document.addEventListener('DOMContentLoaded', () => {
    // Loader
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });

    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Smooth Scrolling & Close Menu on Click
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                const icon = menuToggle.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    });

    // Scroll Animations (Intersection Observer)
    const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // Form Handling
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Basic UI feedback
            const btn = contactForm.querySelector('button[type="submit"]');
            const originalIcon = btn.querySelector('i').className;
            const originalText = btn.querySelector('span').innerText;

            btn.disabled = true;
            btn.querySelector('span').innerText = 'جاري الإرسال...';
            btn.querySelector('i').className = 'fas fa-spinner fa-spin';

            const formData = new FormData(contactForm);

            try {
                const response = await fetch('/contact', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.status === 'success') {
                    formMessage.innerText = result.message;
                    formMessage.className = 'form-message success';
                    contactForm.reset();
                } else {
                    throw new Error('Something went wrong');
                }
            } catch (error) {
                formMessage.innerText = 'حدث خطأ أثناء الإرسال. يرجى المحاولة لاحقاً.';
                formMessage.className = 'form-message error';
            } finally {
                btn.disabled = false;
                btn.querySelector('span').innerText = originalText;
                btn.querySelector('i').className = originalIcon;

                // Clear message after 5 seconds
                setTimeout(() => {
                    formMessage.innerText = '';
                    formMessage.className = 'form-message';
                }, 5000);
            }
        });
    }
    // News Modal Logic
    const modal = document.getElementById("newsModal");
    const closeModal = document.querySelector(".close-modal");

    // Expose function to global scope so onclick in HTML works
    window.openNewsModal = function (element) {
        const title = element.getAttribute('data-title');
        const date = element.getAttribute('data-date');
        const text = element.getAttribute('data-text').replace(/\n/g, '<br>');
        const imageSrc = element.getAttribute('data-image');
        const videoSrc = element.getAttribute('data-video');

        document.getElementById("modalTitle").innerText = title;
        document.getElementById("modalDate").innerText = date;
        document.getElementById("modalText").innerHTML = text;

        const modalImg = document.getElementById("modalImg");
        const modalVideo = document.getElementById("modalVideo");
        const modalVideoSource = document.getElementById("modalVideoSource");
        
        // Show video if available, otherwise show image
        if (videoSrc) {
            modalVideoSource.src = videoSrc;
            modalVideo.load();
            modalVideo.style.display = "block";
            modalImg.style.display = "none";
        } else if (imageSrc) {
            modalImg.src = imageSrc;
            modalImg.style.display = "block";
            modalVideo.style.display = "none";
        } else {
            modalImg.style.display = "none";
            modalVideo.style.display = "none";
        }

        modal.style.display = "flex";
        setTimeout(() => {
            modal.classList.add("show");
        }, 10);
    }

    if (closeModal) {
        closeModal.onclick = function () {
            modal.classList.remove("show");
            setTimeout(() => {
                modal.style.display = "none";
            }, 300);
        }
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.classList.remove("show");
            setTimeout(() => {
                modal.style.display = "none";
            }, 300);
        }
    }
});
