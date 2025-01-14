import { ref } from 'vue';

export function useTooltip() {
    const isTooltipVisible = ref(false);

    const showTooltip = () => {
        isTooltipVisible.value = true;
    };

    const hideTooltip = () => {
        isTooltipVisible.value = false;
    };

    const toggleTooltip = () => {
        isTooltipVisible.value = !isTooltipVisible.value;
    };

    return {
        isTooltipVisible,
        showTooltip,
        hideTooltip,
        toggleTooltip,
    };
}