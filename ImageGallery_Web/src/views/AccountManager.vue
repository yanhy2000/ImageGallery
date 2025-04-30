<template>

</template>

<script>
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import axios from "axios";
import {
    cachePhoto,
    getCachedPhoto,
    cleanExpiredPhotos,
    refreshCache,
} from "@/services/cacheService";


</script>

<style>
</style>
