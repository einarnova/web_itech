// main.js - ScrollSpy y Mejoras de Experiencia de Usuario (UX) para ITECH
document.addEventListener('DOMContentLoaded', () => {
    // 1. Mejorar dinámicamente los ítems de navegación rápida con badges numéricos modernos
    const navLinks = document.querySelectorAll('.sidebar-link');
    navLinks.forEach((link) => {
        const text = link.textContent.trim();
        const match = text.match(/^(\d+)[\.\s]+(.*)$/);
        if (match) {
            const num = match[1].padStart(2, '0');
            const label = match[2];
            link.innerHTML = `<span class="nav-badge">${num}</span><span class="nav-label">${label}</span>`;
        }
    });

    // 2. ScrollSpy Interactivo: Resalta la sección activa durante el scroll
    const sections = Array.from(document.querySelectorAll('section[id]'));
    if (!sections.length || !navLinks.length) return;

    function updateActiveNav() {
        const scrollPosition = window.scrollY || window.pageYOffset;
        const offset = 140; // Compensación por sticky header (80px) + margen de lectura
        let currentSectionId = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop - offset;
            const sectionHeight = section.offsetHeight;
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSectionId = section.getAttribute('id');
            }
        });

        // Si el usuario llega al final de la página, activa la última sección visible
        if ((window.innerHeight + scrollPosition) >= document.body.offsetHeight - 80) {
            const last = sections[sections.length - 1];
            if (last) currentSectionId = last.getAttribute('id');
        }

        // Si está al inicio y aún no alcanza el offset, selecciona el primer ítem
        if (scrollPosition < 250 && navLinks[0]) {
            const firstNavTarget = navLinks[0].getAttribute('href')?.replace('#', '');
            if (firstNavTarget && !currentSectionId) {
                currentSectionId = firstNavTarget;
            }
        }

        navLinks.forEach(link => {
            const targetId = link.getAttribute('href')?.replace('#', '');
            if (targetId && targetId === currentSectionId) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Scroll listener optimizado con requestAnimationFrame
    let isTicking = false;
    window.addEventListener('scroll', () => {
        if (!isTicking) {
            window.requestAnimationFrame(() => {
                updateActiveNav();
                isTicking = false;
            });
            isTicking = true;
        }
    }, { passive: true });

    // Ejecutar al inicio para activar el primer ítem correspondiente
    updateActiveNav();

    // 3. Smooth scroll de precisión al hacer clic
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    navLinks.forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                    const targetTop = target.offsetTop - 90;
                    window.scrollTo({
                        top: targetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // 4. Sistema de Pestañas Interactivas de Filtrado (Servicios Help Desk B2B)
    const tabButtons = document.querySelectorAll('.b2b-tab-btn');
    const serviceCards = document.querySelectorAll('.whitespace-grid .whitespace-card');

    if (tabButtons.length && serviceCards.length) {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.getAttribute('data-tab');

                // Actualizar botón activo
                tabButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Filtrar tarjetas
                serviceCards.forEach(card => {
                    const cardCategory = card.getAttribute('data-category');
                    if (category === 'todos' || cardCategory === category) {
                        card.classList.remove('is-hidden');
                        card.classList.remove('fade-in');
                        void card.offsetWidth; // Forzar reflow para reiniciar animación
                        card.classList.add('fade-in');
                    } else {
                        card.classList.add('is-hidden');
                        card.classList.remove('fade-in');
                    }
                });
            });
        });
    }

    // 5. Alternador de Pestañas de Planes B2B (Abono Mensual vs Servicios On-Demand por Lote)
    const planToggleBtns = document.querySelectorAll('.plans-toggle-btn');
    const planPanes = document.querySelectorAll('.plans-view-pane');

    if (planToggleBtns.length && planPanes.length) {
        planToggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetViewId = btn.getAttribute('data-view');
                planToggleBtns.forEach(b => b.classList.remove('active'));
                planPanes.forEach(pane => pane.classList.remove('active'));

                btn.classList.add('active');
                const targetPane = document.getElementById(targetViewId);
                if (targetPane) {
                    targetPane.classList.add('active');
                }
            });
        });
    }

    // 6. Vinculación Inteligente entre Tarjetas de Servicio y Cotizador Zen UX
    const quoteButtons = document.querySelectorAll('.btn-card-quote');
    quoteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetChipValue = btn.getAttribute('data-service-chip');
            const contactSection = document.getElementById('contacto');

            if (contactSection) {
                const targetTop = contactSection.offsetTop - 85;
                window.scrollTo({
                    top: targetTop,
                    behavior: 'smooth'
                });
            }

            if (targetChipValue) {
                const chips = document.querySelectorAll('#chipServicio .zen-chip');
                chips.forEach(chip => {
                    if (chip.getAttribute('data-value') === targetChipValue) {
                        chips.forEach(c => c.classList.remove('selected'));
                        chip.classList.add('selected');
                        // Efecto visual de pulso
                        chip.style.transform = 'scale(1.08)';
                        setTimeout(() => {
                            chip.style.transform = '';
                        }, 250);
                    }
                });
            }
        });
    });

    // 7. Toggle del Menú Móvil en Header
    const mobileToggle = document.querySelector('.mobile-nav-toggle');
    const headerNav = document.querySelector('.header-nav');

    if (mobileToggle && headerNav) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            headerNav.classList.toggle('nav-open');
        });

        // Cerrar menú móvil al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!headerNav.contains(e.target) && !mobileToggle.contains(e.target)) {
                headerNav.classList.remove('nav-open');
            }
        });

        // Soporte táctil para menús desplegables en móviles
        const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');
        dropdownItems.forEach(item => {
            const link = item.querySelector('.nav-link');
            if (link) {
                link.addEventListener('click', (e) => {
                    if (window.innerWidth <= 960) {
                        e.preventDefault();
                        item.classList.toggle('dropdown-active');
                    }
                });
            }
        });
    }

    // 8. Prevención de solapamiento: El Sidebar se detiene con precisión milimétrica al tocar el Footer
    const sidebar = document.querySelector('.sidebar');
    const footer = document.querySelector('.site-footer');

    if (sidebar && footer) {
        function adjustSidebarPosition() {
            if (window.innerWidth <= 960) {
                sidebar.style.transform = '';
                return;
            }

            const footerRect = footer.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            // Si el footer entra en el viewport visible
            if (footerRect.top < windowHeight) {
                const overlap = windowHeight - footerRect.top;
                sidebar.style.transform = `translateY(-${overlap}px)`;
            } else {
                sidebar.style.transform = 'translateY(0)';
            }
        }

        window.addEventListener('scroll', adjustSidebarPosition, { passive: true });
        window.addEventListener('resize', adjustSidebarPosition, { passive: true });
        adjustSidebarPosition();
    }
});

