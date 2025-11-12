class ActivityWheel {
    constructor() {
        this.wheelItems = document.getElementById('wheel-items');
        this.items = Array.from(document.querySelectorAll('.wheel-item'));
        this.currentIndex = this.findTodayIndex();
        this.itemHeight = 120; // Base height for spacing

        this.init();
    }

    findTodayIndex() {
        const todayItem = this.items.findIndex(item => item.classList.contains('today'));
        // Default to last item (most recent) if no "today" found
        return todayItem >= 0 ? todayItem : Math.max(0, this.items.length - 1);
    }

    init() {
        // Check if wheel elements exist (they won't if we're before start date)
        const prevBtn = document.getElementById('wheel-prev');
        const nextBtn = document.getElementById('wheel-next');

        if (!prevBtn || !nextBtn || this.items.length === 0) {
            return; // No wheel to initialize
        }

        // Set up navigation buttons
        prevBtn.addEventListener('click', () => this.rotate(-1));
        nextBtn.addEventListener('click', () => this.rotate(1));

        // Support mouse wheel scrolling
        this.wheelItems.addEventListener('wheel', (e) => {
            e.preventDefault();
            const direction = e.deltaY > 0 ? 1 : -1;
            this.rotate(direction);
        }, { passive: false });

        // Support clicking on items to select them
        this.items.forEach((item, index) => {
            item.addEventListener('click', (e) => {
                // Don't interfere with checkbox clicks
                if (!e.target.closest('input[type="checkbox"]')) {
                    const diff = index - this.currentIndex;
                    if (diff !== 0) {
                        this.currentIndex = index;
                        this.updateWheel();
                    }
                }
            });
        });

        // Support keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.rotate(-1);
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.rotate(1);
            }
        });

        // Initial render
        this.updateWheel();

        // Listen for HTMX updates to refresh wheel
        document.body.addEventListener('htmx:afterSwap', () => {
            // Re-query items in case they were updated
            this.items = Array.from(document.querySelectorAll('.wheel-item'));
            this.updateWheel();
        });
    }

    rotate(direction) {
        this.currentIndex += direction;

        // Clamp to valid range
        if (this.currentIndex < 0) {
            this.currentIndex = 0;
        } else if (this.currentIndex >= this.items.length) {
            this.currentIndex = this.items.length - 1;
        }

        this.updateWheel();
    }

    updateWheel() {
        const viewportHeight = this.wheelItems.parentElement.offsetHeight;
        const centerY = viewportHeight / 2;

        this.items.forEach((item, index) => {
            const offset = index - this.currentIndex;
            // Shift everything down by one item height to show previous item above
            const posY = centerY + (offset * this.itemHeight) + this.itemHeight;

            // Calculate scale and opacity based on distance from center
            const distance = Math.abs(offset);
            let scale, opacity, zIndex;

            if (distance === 0) {
                // Center item - largest
                scale = 1;
                opacity = 1;
                zIndex = 100;
            } else if (distance === 1) {
                scale = 0.85;
                opacity = 0.7;
                zIndex = 90;
            } else if (distance === 2) {
                scale = 0.7;
                opacity = 0.5;
                zIndex = 80;
            } else if (distance === 3) {
                scale = 0.6;
                opacity = 0.3;
                zIndex = 70;
            } else {
                scale = 0.5;
                opacity = 0.15;
                zIndex = 60;
            }

            // Apply transforms
            item.style.transform = `translateY(${posY - centerY}px) scale(${scale})`;
            item.style.opacity = opacity;
            item.style.zIndex = zIndex;
            item.style.pointerEvents = distance > 3 ? 'none' : 'auto';

            // Update visual state for center item
            if (distance === 0) {
                item.style.boxShadow = '0 12px 32px rgba(102, 126, 234, 0.4)';
            } else {
                if (item.classList.contains('today')) {
                    item.style.boxShadow = '0 8px 24px rgba(102, 126, 234, 0.3)';
                } else {
                    item.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
                }
            }
        });

        // Update button states
        const prevBtn = document.getElementById('wheel-prev');
        const nextBtn = document.getElementById('wheel-next');

        prevBtn.disabled = this.currentIndex === 0;
        nextBtn.disabled = this.currentIndex === this.items.length - 1;

        prevBtn.style.opacity = prevBtn.disabled ? '0.5' : '1';
        nextBtn.style.opacity = nextBtn.disabled ? '0.5' : '1';
        prevBtn.style.cursor = prevBtn.disabled ? 'not-allowed' : 'pointer';
        nextBtn.style.cursor = nextBtn.disabled ? 'not-allowed' : 'pointer';
    }
}

// Initialize the wheel when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ActivityWheel();
});
