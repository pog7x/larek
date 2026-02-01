'use strict';

/**
 * Larek Marketplace - Main Application JavaScript
 * Vanilla JS only, no jQuery dependencies
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    App.init();
});

const App = {
    init: function() {
        this.initSwiper();
        this.initPriceRange();
        this.initPhoneMask();
        this.initMobileMenu();
        this.initCategoriesDropdown();
        this.initBootstrapDropdowns();
        this.initNavbarCollapse();
        this.initCountdown();
        this.initHtmxEvents();
        this.initSearchToggle();
        this.initProfileDropdown();
    },

    /**
     * Initialize Swiper sliders
     */
    initSwiper: function() {
        // Main hero slider
        const heroSlider = document.querySelector('.hero-slider');
        if (heroSlider) {
            new Swiper(heroSlider, {
                loop: true,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
            });
        }

        // Product carousel slider
        const carouselSliders = document.querySelectorAll('.product-carousel');
        carouselSliders.forEach(function(slider) {
            new Swiper(slider, {
                slidesPerView: 1,
                spaceBetween: 20,
                navigation: {
                    nextEl: slider.querySelector('.swiper-button-next'),
                    prevEl: slider.querySelector('.swiper-button-prev'),
                },
                pagination: {
                    el: slider.querySelector('.swiper-pagination'),
                    clickable: true,
                },
                breakpoints: {
                    576: {
                        slidesPerView: 2,
                    },
                    992: {
                        slidesPerView: 3,
                    },
                    1400: {
                        slidesPerView: 4,
                    },
                },
            });
        });

        // Product detail gallery
        const productGallery = document.querySelector('.product-gallery');
        if (productGallery) {
            const thumbsSwiper = new Swiper('.product-thumbs', {
                spaceBetween: 10,
                slidesPerView: 4,
                freeMode: true,
                watchSlidesProgress: true,
            });

            new Swiper(productGallery, {
                spaceBetween: 10,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                thumbs: {
                    swiper: thumbsSwiper,
                },
            });
        }
    },

    /**
     * Initialize price range slider using noUiSlider
     */
    initPriceRange: function() {
        const priceSlider = document.getElementById('price-range');
        if (priceSlider && typeof noUiSlider !== 'undefined') {
            const minInput = document.querySelector('input[name="price_gte"]');
            const maxInput = document.querySelector('input[name="price_lte"]');
            
            const minVal = parseFloat(priceSlider.dataset.min) || 0;
            const maxVal = parseFloat(priceSlider.dataset.max) || 10000;
            const startMin = parseFloat(minInput?.value) || minVal;
            const startMax = parseFloat(maxInput?.value) || maxVal;

            noUiSlider.create(priceSlider, {
                start: [startMin, startMax],
                connect: true,
                range: {
                    'min': minVal,
                    'max': maxVal
                },
                format: {
                    to: function(value) {
                        return Math.round(value);
                    },
                    from: function(value) {
                        return Number(value);
                    }
                }
            });

            const priceDisplay = document.getElementById('price-display');

            priceSlider.noUiSlider.on('update', function(values) {
                if (minInput) minInput.value = values[0];
                if (maxInput) maxInput.value = values[1];
                if (priceDisplay) {
                    priceDisplay.textContent = `$${values[0]} - $${values[1]}`;
                }
            });
        }
    },

    /**
     * Initialize phone input mask using iMask
     */
    initPhoneMask: function() {
        const phoneInputs = document.querySelectorAll('[data-mask="phone"]');
        if (typeof IMask !== 'undefined') {
            phoneInputs.forEach(function(input) {
                IMask(input, {
                    mask: '+{7} (000) 000-00-00'
                });
            });
        }

        // Card number mask
        const cardInputs = document.querySelectorAll('[data-mask="card"]');
        if (typeof IMask !== 'undefined') {
            cardInputs.forEach(function(input) {
                IMask(input, {
                    mask: '0000 0000 0000 0000'
                });
            });
        }
    },

    /**
     * Mobile menu toggle
     */
    initMobileMenu: function() {
        const toggler = document.querySelector('.navbar-toggler');
        const menu = document.querySelector('.navbar-collapse');
        
        if (toggler && menu) {
            toggler.addEventListener('click', function() {
                menu.classList.toggle('show');
            });

            // Close menu when clicking outside
            document.addEventListener('click', function(e) {
                if (!menu.contains(e.target) && !toggler.contains(e.target)) {
                    menu.classList.remove('show');
                }
            });
        }
    },

    /**
     * Categories dropdown menu
     */
    initCategoriesDropdown: function() {
        const dropdowns = document.querySelectorAll('.categories-dropdown');
        dropdowns.forEach(function(dropdown) {
            const trigger = dropdown.querySelector('.categories-trigger');
            const content = dropdown.querySelector('.categories-content');

            if (trigger && content) {
                trigger.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Close other dropdowns
                    document.querySelectorAll('.categories-dropdown.open').forEach(function(d) {
                        if (d !== dropdown) d.classList.remove('open');
                    });
                    
                    dropdown.classList.toggle('open');
                });
            }
        });

        // Close when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.categories-dropdown')) {
                document.querySelectorAll('.categories-dropdown.open').forEach(function(d) {
                    d.classList.remove('open');
                });
            }
        });
    },

    /**
     * Initialize Bootstrap dropdowns manually (for HTMX compatibility)
     */
    initBootstrapDropdowns: function() {
        const dropdownTriggers = document.querySelectorAll('[data-bs-toggle="dropdown"]');
        dropdownTriggers.forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const menu = trigger.nextElementSibling;
                if (menu && menu.classList.contains('dropdown-menu')) {
                    // Close other dropdowns
                    document.querySelectorAll('.dropdown-menu.show').forEach(function(m) {
                        if (m !== menu) m.classList.remove('show');
                    });
                    menu.classList.toggle('show');
                }
            });
        });

        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.show').forEach(function(m) {
                    m.classList.remove('show');
                });
            }
        });
    },

    /**
     * Initialize Bootstrap navbar collapse
     */
    initNavbarCollapse: function() {
        const togglers = document.querySelectorAll('[data-bs-toggle="collapse"]');
        togglers.forEach(function(toggler) {
            toggler.addEventListener('click', function(e) {
                const targetSelector = toggler.getAttribute('data-bs-target');
                const target = document.querySelector(targetSelector);
                if (target) {
                    target.classList.toggle('show');
                }
            });
        });
    },

    /**
     * Countdown timer for limited offers
     */
    initCountdown: function() {
        const countdowns = document.querySelectorAll('[data-countdown]');
        
        countdowns.forEach(function(el) {
            const endDate = el.dataset.countdown;
            if (!endDate) return;

            function updateCountdown() {
                const parts = endDate.split(' ');
                const dateParts = parts[0].split('.');
                const timeParts = parts[1] ? parts[1].split(':') : ['0', '0'];
                
                const target = new Date(
                    dateParts[2], 
                    dateParts[1] - 1, 
                    dateParts[0], 
                    timeParts[0], 
                    timeParts[1]
                );
                
                const now = new Date();
                const diff = target - now;

                if (diff <= 0) {
                    el.innerHTML = '<span class="text-danger">Expired</span>';
                    return;
                }

                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((diff % (1000 * 60)) / 1000);

                const daysEl = el.querySelector('.countdown-days');
                const hoursEl = el.querySelector('.countdown-hours');
                const minutesEl = el.querySelector('.countdown-minutes');
                const secondsEl = el.querySelector('.countdown-seconds');

                if (daysEl) daysEl.textContent = days;
                if (hoursEl) hoursEl.textContent = hours;
                if (minutesEl) minutesEl.textContent = minutes;
                if (secondsEl) secondsEl.textContent = seconds;
            }

            updateCountdown();
            setInterval(updateCountdown, 1000);
        });
    },

    /**
     * HTMX event handlers
     */
    initHtmxEvents: function() {
        // Re-initialize components after HTMX swaps
        document.body.addEventListener('htmx:afterSwap', function(e) {
            // Re-init countdowns if new ones appeared
            App.initCountdown();
            
            // Re-init Swiper if new sliders appeared
            App.initSwiper();
        });

        // Show loading indicator
        document.body.addEventListener('htmx:beforeRequest', function(e) {
            const indicator = e.detail.elt.querySelector('.htmx-indicator');
            if (indicator) {
                indicator.style.display = 'inline-block';
            }
        });

        // Hide loading indicator
        document.body.addEventListener('htmx:afterRequest', function(e) {
            const indicator = e.detail.elt.querySelector('.htmx-indicator');
            if (indicator) {
                indicator.style.display = 'none';
            }
        });
    },

    /**
     * Search bar toggle on mobile
     */
    initSearchToggle: function() {
        const searchToggle = document.querySelector('.search-toggle');
        const searchForm = document.querySelector('.search-form');

        if (searchToggle && searchForm) {
            searchToggle.addEventListener('click', function(e) {
                e.preventDefault();
                searchForm.classList.toggle('show');
            });
        }
    },

    /**
     * Profile dropdown menu
     */
    initProfileDropdown: function() {
        const dropdown = document.querySelector('.profile-dropdown');
        if (dropdown) {
            const trigger = dropdown.querySelector('.profile-trigger');
            const menu = dropdown.querySelector('.dropdown-menu');

            if (trigger && menu) {
                trigger.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    menu.classList.toggle('show');
                });

                document.addEventListener('click', function(e) {
                    if (!dropdown.contains(e.target)) {
                        menu.classList.remove('show');
                    }
                });
            }
        }
    }
};

/**
 * Utility functions
 */
const Utils = {
    /**
     * Format price with commas
     */
    formatPrice: function(price) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    /**
     * Debounce function
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = function() {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Show toast notification
     */
    showToast: function(message, type = 'success') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0 show`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);

        // Auto remove after 3 seconds
        setTimeout(function() {
            toast.remove();
        }, 3000);

        // Close button
        toast.querySelector('.btn-close').addEventListener('click', function() {
            toast.remove();
        });
    }
};
