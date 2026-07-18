// Mobile Navigation
const hamburger = document.querySelector(".menu-toggle");
const navMenu = document.querySelector(".nav-menu");

if (hamburger && navMenu) {
    hamburger.addEventListener("click", () => {
        navMenu.classList.toggle("active");
        hamburger.classList.toggle("active");
    });

    document.querySelectorAll(".nav-menu a").forEach((link) => {
        link.addEventListener("click", () => {
            navMenu.classList.remove("active");
            hamburger.classList.remove("active");
        });
    });
}

// Theme Toggle
const themeToggle = document.getElementById("theme-toggle");
const body = document.body;
const themeStorageKey = "portifolio-theme";

const getStoredTheme = () => {
    const storedTheme = localStorage.getItem(themeStorageKey);
    if (storedTheme === "light" || storedTheme === "dark") {
        return storedTheme;
    }

    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches
        ? "light"
        : "dark";
};

const applyTheme = (theme) => {
    body.classList.toggle("light-theme", theme === "light");
    localStorage.setItem(themeStorageKey, theme);
    if (themeToggle) {
        themeToggle.setAttribute("aria-pressed", theme === "light");
        themeToggle.setAttribute("title", theme === "light" ? "Switch to dark mode" : "Switch to light mode");
    }
};

applyTheme(getStoredTheme());

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        const nextTheme = body.classList.contains("light-theme") ? "dark" : "light";
        applyTheme(nextTheme);
    });
}

// Animate skill bars and reveal content as it enters view
const skillBars = document.querySelectorAll(".skill-progress");
const revealItems = document.querySelectorAll(".reveal-on-scroll");

const observerOptions = {
    threshold: 0.2,
    rootMargin: "0px 0px -10% 0px"
};

const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

revealItems.forEach((item) => {
    item.classList.add("reveal-on-scroll");
    revealObserver.observe(item);
});

window.revealObserver = revealObserver;
window.addEventListener('github-repos-loaded', () => {
    document.querySelectorAll('.project-card.reveal-on-scroll').forEach((card) => {
        revealObserver.observe(card);
    });
});

const skillObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            const bar = entry.target;
            const width = bar.getAttribute("data-width");
            if (width) {
                bar.style.width = width;
            }
            observer.unobserve(bar);
        }
    });
}, observerOptions);

skillBars.forEach((bar) => skillObserver.observe(bar));

// Form submission
const contactForm = document.getElementById("contactForm");

if (contactForm) {
    contactForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitButton = contactForm.querySelector("button[type='submit']");
        const originalText = submitButton ? submitButton.innerHTML : "";
        const formData = new FormData(contactForm);
        const payload = Object.fromEntries(formData.entries());

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin" aria-hidden="true"></i> Sending...';
        }

        try {
            const isLocalDev = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
            const endpoint = isLocalDev ? "/api/contact" : "https://formsubmit.co/ajax/daudki044@gmail.com";

            let response;
            let result;

            if (isLocalDev) {
                response = await fetch(endpoint, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                result = await response.json();
            } else {
                const params = new URLSearchParams();
                Object.entries(payload).forEach(([key, value]) => params.append(key, value));
                params.append("_subject", payload.subject || "Portfolio contact form");
                params.append("_replyto", payload.email || "");
                params.append("_next", window.location.href);
                response = await fetch(endpoint, {
                    method: "POST",
                    headers: { "Accept": "application/json" },
                    body: params
                });
                result = await response.json();
            }

            if (!response.ok) {
                throw new Error(result.message || "Unable to send your message right now.");
            }

            contactForm.reset();
            const successMessage = document.createElement("p");
            successMessage.className = "form-success";
            successMessage.textContent = "Thank you! Your message has been received.";
            contactForm.appendChild(successMessage);
            setTimeout(() => successMessage.remove(), 5000);
        } catch (error) {
            const errorMessage = document.createElement("p");
            errorMessage.className = "form-error";
            errorMessage.textContent = error.message || "Something went wrong while sending your message.";
            contactForm.appendChild(errorMessage);
            setTimeout(() => errorMessage.remove(), 5000);
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            }
        }
    });
}

// Add active class to nav links based on scroll position
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-menu a");

window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute("id");
        }
    });

    navLinks.forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href").substring(1) === current) {
            link.classList.add("active");
        }
    });
});

const year = document.getElementById("year");
if (year) {
    year.textContent = new Date().getFullYear();
}

// Cursor bubble trail effect for creative UX
let lastBubbleTime = 0;
const createCursorBubble = (x, y) => {
    const bubble = document.createElement('span');
    bubble.className = 'cursor-bubble';
    const size = Math.floor(Math.random() * 12) + 10;
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;
    bubble.style.left = `${x}px`;
    bubble.style.top = `${y}px`;
    bubble.style.background = `radial-gradient(circle, rgba(56, 189, 248, 0.85), rgba(59, 130, 246, 0.08))`;
    bubble.style.boxShadow = `0 0 24px rgba(56, 189, 248, 0.24)`;
    document.body.appendChild(bubble);

    window.setTimeout(() => {
        bubble.remove();
    }, 900);
};

document.addEventListener('mousemove', (event) => {
    if (window.innerWidth <= 760) return;
    const now = performance.now();
    if (now - lastBubbleTime < 60) return;
    lastBubbleTime = now;
    createCursorBubble(event.clientX, event.clientY);
});
