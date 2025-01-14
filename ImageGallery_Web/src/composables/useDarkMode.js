import { ref, onMounted } from 'vue';

export function useDarkMode() {
    const DarkMode = ref(false);

    const toggleDarkMode = () => {
        DarkMode.value = !DarkMode.value;
        if (DarkMode.value) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    };

    const checkDarkMode = () => {
        const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');
        if (prefersDarkMode.matches) {
            DarkMode.value = true;
            document.body.classList.add('dark-mode');
        } else {
            DarkMode.value = false;
            document.body.classList.remove('dark-mode');
        }
        prefersDarkMode.addEventListener('change', () => { });
    };

    onMounted(() => {
        checkDarkMode();
    });

    return {
        DarkMode,
        toggleDarkMode,
    };
}