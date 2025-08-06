import { reactive } from "vue";

export const themeStore = reactive({
    isDark: false,
    toggleTheme() {
        this.isDark = !this.isDark;
        document.documentElement.classList.toggle('dark', this.isDark);
        localStorage.setItem('theme', this.isDark ? 'dark' : 'light');
    }
});