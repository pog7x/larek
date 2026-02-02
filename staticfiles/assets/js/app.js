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
        var self = this;
        var inits = [
            'initSwiper',
            'initPriceRange',
            'initPhoneMask',
            'initCategoriesDropdown',
            'initBootstrapDropdowns',
            'initNavbarCollapse',
            'initCountdown',
            'initHtmxEvents',
            'initSearchToggle'
        ];
        inits.forEach(function(fn) {
            try {
                self[fn]();
            } catch (e) {
                console.error('Error in ' + fn + ':', e);
            }
        });
    },

    /**
     * Initialize Swiper sliders
     */
    initSwiper: function() {
        // Helper to check if Swiper is already initialized
        function isInitialized(el) {
            return el && el.classList.contains('swiper-initialized');
        }

        // Main hero slider - use correct selector for swiper container
        const heroSlider = document.querySelector('.hero-slider-swiper');
        if (heroSlider && !isInitialized(heroSlider)) {
            new Swiper(heroSlider, {
                loop: true,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: heroSlider.querySelector('.swiper-pagination'),
                    clickable: true,
                },
                navigation: {
                    nextEl: heroSlider.querySelector('.swiper-button-next'),
                    prevEl: heroSlider.querySelector('.swiper-button-prev'),
                },
                effect: 'fade',
                fadeEffect: {
                    crossFade: true
                }
            });
        }

        // Product carousel slider
        const carouselSliders = document.querySelectorAll('.product-carousel');
        carouselSliders.forEach(function(slider) {
            if (isInitialized(slider)) return;

            // Find navigation buttons - check inside slider first, then in parent container
            var parent = slider.closest('section') || slider.parentElement;
            var nextBtn = slider.querySelector('.swiper-button-next') || 
                          (parent ? parent.querySelector('[class*="swiper-button-next"]') : null);
            var prevBtn = slider.querySelector('.swiper-button-prev') || 
                          (parent ? parent.querySelector('[class*="swiper-button-prev"]') : null);
            var pagination = slider.querySelector('.swiper-pagination');

            new Swiper(slider, {
                slidesPerView: 1,
                spaceBetween: 20,
                navigation: {
                    nextEl: nextBtn,
                    prevEl: prevBtn,
                },
                pagination: pagination ? {
                    el: pagination,
                    clickable: true,
                } : false,
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
        const productThumbs = document.querySelector('.product-thumbs');
        if (productGallery && !isInitialized(productGallery)) {
            var thumbsSwiper = null;
            if (productThumbs && !isInitialized(productThumbs)) {
                thumbsSwiper = new Swiper(productThumbs, {
                    spaceBetween: 10,
                    slidesPerView: 4,
                    freeMode: true,
                    watchSlidesProgress: true,
                });
            }

            new Swiper(productGallery, {
                spaceBetween: 10,
                navigation: {
                    nextEl: productGallery.querySelector('.swiper-button-next'),
                    prevEl: productGallery.querySelector('.swiper-button-prev'),
                },
                thumbs: thumbsSwiper ? {
                    swiper: thumbsSwiper,
                } : undefined,
            });
        }
    },

    /**
     * Initialize price range slider using noUiSlider
     */
    initPriceRange: function() {
        const priceSlider = document.getElementById('price-range');
        if (!priceSlider || typeof noUiSlider === 'undefined') return;

        if (priceSlider.noUiSlider) {
            priceSlider.noUiSlider.destroy();
        }

        const minInput = document.querySelector('input[name="price_gte"]');
        const maxInput = document.querySelector('input[name="price_lte"]');
        const minVal = parseFloat(priceSlider.dataset.min) || 0;
        const maxVal = parseFloat(priceSlider.dataset.max) || 10000;
        const startMin = parseFloat(minInput ? minInput.value : null) || minVal;
        const startMax = parseFloat(maxInput ? maxInput.value : null) || maxVal;

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
                priceDisplay.textContent = '$' + values[0] + ' - $' + values[1];
            }
        });
    },

    /**
     * Initialize phone input mask using iMask
     */
    initPhoneMask: function() {
        if (typeof IMask === 'undefined') return;

        const phoneInputs = document.querySelectorAll('[data-mask="phone"]');
        phoneInputs.forEach(function(input) {
            IMask(input, {
                mask: '+{7} (000) 000-00-00'
            });
        });

        // Card number mask
        const cardInputs = document.querySelectorAll('[data-mask="card"]');
        cardInputs.forEach(function(input) {
            IMask(input, {
                mask: '0000 0000 0000 0000'
            });
        });

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
     * Initialize Bootstrap navbar collapse (burger menu)
     */
    initNavbarCollapse: function() {
        var toggler = document.querySelector('[data-bs-toggle="collapse"]');
        var menu = toggler ? document.querySelector(toggler.getAttribute('data-bs-target')) : null;
        if (!toggler || !menu) return;

        document.addEventListener('click', function(e) {
            var trigger = e.target.closest('[data-bs-toggle="collapse"]');
            if (trigger) {
                e.preventDefault();
                e.stopPropagation();
                menu.classList.toggle('show');
                toggler.setAttribute('aria-expanded', menu.classList.contains('show'));
                return;
            }

            if (!menu.contains(e.target) && !toggler.contains(e.target)) {
                menu.classList.remove('show');
                toggler.setAttribute('aria-expanded', 'false');
            }
        });
    },

    /**
     * Countdown timer for limited offers
     */
    initCountdown: function() {
        const countdowns = document.querySelectorAll('[data-countdown]');
        if (!countdowns.length) return;

        const parsedCountdowns = [];

        countdowns.forEach(function(el) {
            const endDate = el.dataset.countdown;
            if (!endDate) return;

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

            parsedCountdowns.push({
                el: el,
                target: target
            });
        });

        if (!parsedCountdowns.length) return;

        function updateAllCountdowns() {
            const now = new Date();

            parsedCountdowns.forEach(function(item) {
                const diff = item.target - now;
                const el = item.el;

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
            });
        }

        updateAllCountdowns();
        setInterval(updateAllCountdowns, 1000);
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
        var section = document.getElementById('search-bar-section');
        if (!section) return;

        document.addEventListener('click', function(e) {
            var toggle = e.target.closest('.search-toggle');
            if (toggle) {
                e.preventDefault();
                e.stopPropagation();
                section.classList.toggle('is-open');
                return;
            }
            if (section.classList.contains('is-open') && !section.contains(e.target)) {
                section.classList.remove('is-open');
            }
        });
    },

    
    
};

/**
 * Utility functions
 */
const Utils = {
    /**
     * Format price with commas
     */
    formatPrice: function(price) {
        return Number(price).toLocaleString('en-US');
    },

    /**
     * Debounce function
     */
    debounce: function(func, wait) {
        var timeout;
        return function() {
            var context = this;
            var args = arguments;
            var later = function() {
                clearTimeout(timeout);
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Show toast notification
     */
    showToast: function(message, type) {
        type = type || 'success';
        var toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;

        var toast = document.createElement('div');
        toast.className = 'toast align-items-center text-bg-' + type + ' border-0 show';
        toast.setAttribute('role', 'alert');

        var toastInner = document.createElement('div');
        toastInner.className = 'd-flex';

        var toastBody = document.createElement('div');
        toastBody.className = 'toast-body';
        toastBody.textContent = String(message);

        var closeButton = document.createElement('button');
        closeButton.type = 'button';
        closeButton.className = 'btn-close btn-close-white me-2 m-auto';
        closeButton.setAttribute('data-bs-dismiss', 'toast');
        closeButton.setAttribute('aria-label', 'Close');

        toastInner.appendChild(toastBody);
        toastInner.appendChild(closeButton);
        toast.appendChild(toastInner);
        
        toastContainer.appendChild(toast);

        setTimeout(function() {
            toast.remove();
        }, 3000);

        toast.querySelector('.btn-close').addEventListener('click', function() {
            toast.remove();
        });
    }
};
