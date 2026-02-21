<template>
    <div class="step-card">
        <!-- Top Right Step Label -->
        <div class="step-badge">
            {{ stepText }}
        </div>

        <!-- Content Section -->
        <div class="card-body">
            <h3 class="card-title">{{ title }}</h3>
            <p class="card-description">{{ description }}</p>

            <!-- Tags Section -->
            <div class="tag-container">
                <span v-for="(tag, index) in tags" :key="index" class="card-tag">
                    {{ tag }}
                </span>
            </div>
            <!-- Action Button -->
            <button class="enter-btn" @click="handleBtnClick">
                <!-- 进入模块 -->
                Enter Module
                <!-- Example usage of TDesign Icons -->
                <chevron-right-icon size="14px" class="icon-suffix" />
            </button>
        </div>
    </div>
</template>

<script>
// Importing an icon from the tdesign-icons-vue-next library
import { ChevronRightIcon } from 'tdesign-icons-vue-next';

export default {
    name: 'StepCard',
    components: {
        ChevronRightIcon,
    },
    props: {
        // Label text like "STEP 01"
        stepText: {
            type: String,
            default: 'STEP 01',
        },
        // Main Title
        title: {
            type: String,
            required: true,
        },
        // Description text
        description: {
            type: String,
            default: '',
        },
        // Array of strings for tags
        tags: {
            type: Array,
            default: () => [],
        },
        // Click callback is handled via an emit or a prop function
        // Using a method to trigger the click logic
    },
    methods: {
        handleBtnClick() {
            // Emit an event to the parent component
            this.$emit('onClick');
        },
    },
};
</script>

<style scoped>
.step-card {
    position: relative;
    width: 320px;
    background-color: var(--yf-color-3);
    /* Dark navy background */
    border: 1px solid #e7e7e7;
    border-radius: 12px;
    padding: 24px;
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-sizing: border-box;
    transition: transform 0.2s ease;
}

.step-card:hover {
    border-color: var(--yf-color-6);
    transform: translateY(-2px);
}

/* Step Badge in Top Right */
.step-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background-color: var(--yf-color-7);
    /* Teal color from image */
    color: var(--yf-color-3);
    font-size: 11px;
    font-weight: bold;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

/* Title Styling */
.card-title {
    color: var(--yf-color-2);
    font-size: 20px;
    margin: 0 0 16px 0;
    font-weight: 600;
    letter-spacing: 1px;
}

/* Description Styling */
.card-description {
    font-size: 13px;
    line-height: 1.6;
    color: #94a3b8;
    /* Muted grey text */
    margin-bottom: 20px;
    /* min-height: 83px; */
    height: 83px;
    text-align: left;
    /* Ensures consistent alignment */
}

/* Tag Container and Tags */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 24px;
}

.card-tag {
    font-size: 12px;
    padding: 4px 12px;
    border: 1px solid rgba(85, 195, 195, 0.3);
    background-color: rgba(85, 195, 195, 0.1);
    color: var(--yf-color-7);
    border-radius: 16px;
    white-space: nowrap;
}

/* Button Styling */
.enter-btn {
    background-color: var(--yf-color-4);
    border: 1px solid var(--yf-color-8);
    color: #ffffff;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    transition: all 0.3s;
}

.enter-btn:hover {
    background-color: var(--yf-color-5);
    /* border-color: var(--yf-color-6); */
}

.icon-suffix {
    margin-left: 4px;
}
</style>