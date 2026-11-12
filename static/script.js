document.addEventListener("DOMContentLoaded", () => {
    // Theme Toggle (Dark Blue Mode <-> Light Mode)
    const themeToggleBtn = document.getElementById("theme-toggle-btn");
    const themeIcon = document.getElementById("theme-icon");
    const themeLabel = document.getElementById("theme-label");

    function updatePlotlyCharts(theme) {
        if (typeof window.Plotly === "undefined") return;
        const isDark = theme === "dark";
        const textColor = isDark ? "#f8fafc" : "#31333f";
        const gridColor = isDark ? "rgba(248, 250, 252, 0.14)" : "rgba(49, 51, 63, 0.12)";
        const accentColor = isDark ? "#60a5fa" : "#0068c9";

        const chartDivs = document.querySelectorAll(".js-plotly-plot");
        chartDivs.forEach((div) => {
            window.Plotly.relayout(div, {
                "font.color": textColor,
                "xaxis.color": textColor,
                "xaxis.gridcolor": gridColor,
                "yaxis.color": textColor,
                "yaxis.gridcolor": gridColor,
            });
            window.Plotly.restyle(div, {
                "marker.color": accentColor,
                "line.color": accentColor,
            });
        });
    }

    function applyThemeUI(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        if (themeIcon && themeLabel) {
            if (theme === "dark") {
                themeIcon.textContent = "☀️";
                themeLabel.textContent = "Light Mode";
            } else {
                themeIcon.textContent = "🌙";
                themeLabel.textContent = "Dark Mode";
            }
        }
        updatePlotlyCharts(theme);
    }

    const initialTheme = document.documentElement.getAttribute("data-theme") || "dark";
    applyThemeUI(initialTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme") || "dark";
            const next = current === "dark" ? "light" : "dark";
            localStorage.setItem("theme", next);
            applyThemeUI(next);
        });
    }

    // Sidebar collapse / expand toggle
    const sidebar = document.getElementById("sidebar");
    const closeBtn = document.getElementById("sidebar-close-btn");
    const openBtn = document.getElementById("sidebar-open-btn");

    if (sidebar && closeBtn && openBtn) {
        closeBtn.addEventListener("click", () => {
            sidebar.classList.add("collapsed");
            document.body.classList.add("sidebar-is-collapsed");
        });

        openBtn.addEventListener("click", () => {
            sidebar.classList.remove("collapsed");
            document.body.classList.remove("sidebar-is-collapsed");
        });
    }

    // Number input stepper buttons (- / +)
    const stepDec = document.getElementById("step-dec");
    const stepInc = document.getElementById("step-inc");
    const amountInput = document.getElementById("amount-input");

    if (stepDec && stepInc && amountInput) {
        stepDec.addEventListener("click", () => {
            const min = parseFloat(amountInput.min) || 0.01;
            const current = parseFloat(amountInput.value) || min;
            const next = Math.max(min, +(current - 0.01).toFixed(2));
            amountInput.value = next.toFixed(2);
        });

        stepInc.addEventListener("click", () => {
            const min = parseFloat(amountInput.min) || 0.01;
            const current = parseFloat(amountInput.value) || 0;
            const next = Math.max(min, +(current + 0.01).toFixed(2));
            amountInput.value = next.toFixed(2);
        });
    }

    // Reactive filter form submission (preserves scroll position)
    const filterForm = document.getElementById("filter-form");
    if (filterForm) {
        const savedScroll = sessionStorage.getItem("expense_tracker_scroll");
        if (savedScroll !== null) {
            window.scrollTo(0, parseInt(savedScroll, 10));
            sessionStorage.removeItem("expense_tracker_scroll");
        }

        const autoSubmitInputs = filterForm.querySelectorAll(".auto-submit");
        autoSubmitInputs.forEach((input) => {
            input.addEventListener("change", () => {
                sessionStorage.setItem("expense_tracker_scroll", String(window.scrollY));
                filterForm.submit();
            });
        });
    }
});
