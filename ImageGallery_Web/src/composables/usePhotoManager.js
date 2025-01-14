import { ref, computed } from 'vue';
import axios from 'axios';
import { cachePhoto, getCachedPhoto, cleanExpiredPhotos } from '@/services/cacheService';

export function usePhotoManager() {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
    const photos = ref([]);
    const currentPage = ref(1);
    const totalPages = ref(1);
    const perPage = ref(6);
    const totalPhotos = ref(0);
    const error = ref(null);

    const fetchPhotos = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/photos_list?page=${currentPage.value}&perpage=${perPage.value}`);

            if (response.status !== 200) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = response.data;

            if (data.code == 200) {
                photos.value = data.data.photos;
                totalPhotos.value = data.data.totalPhotos;
                totalPages.value = data.data.totalPages;
                for (let i = 0; i < photos.value.length; i++) {
                    const photo = photos.value[i];
                    const thumbnailUrl = await fetchThumbnail(photo.photoid);
                    if (thumbnailUrl) {
                        photos.value[i] = { ...photo, thumbnailUrl };
                    }
                }
            } else {
                error.value = data.message;
            }
        } catch (e) {
            console.error('Failed to fetch photos:', e);
            if (e.status == 401) {
                alert('Token unauthorized!');
            }
            error.value = e.message;
        }
    };

    const fetchThumbnail = async (photoId) => {
        try {
            const cachedPhoto = await getCachedPhoto(photoId);

            if (cachedPhoto) {
                console.log(`Using cached thumbnail for photo ${photoId}`);

                if (cachedPhoto.blob) {
                    return URL.createObjectURL(cachedPhoto.blob);
                }

                return cachedPhoto.thumbnailUrl;
            }

            console.log(`Fetching thumbnail for photo ${photoId} from network...`);
            const response = await fetch(`${API_BASE_URL}/api/getphoto?photoid=${photoId}`);
            if (response.ok) {
                const thumbnailBlob = await response.blob();
                const thumbnailUrl = URL.createObjectURL(thumbnailBlob);

                await cachePhoto(photoId, thumbnailUrl, thumbnailBlob);

                return thumbnailUrl;
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (e) {
            console.error(`Failed to fetch thumbnail for photo ${photoId}:`, e);
            return '';
        }
    };

    const getPhotoInfo = async (photoid) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/getphotoinfo?photoid=${photoid}`);
            if (response.data.code === 200) {
                return response.data.data;
            } else {
                alert('Failed to load photo info');
            }
        } catch (error) {
            console.error('Error fetching photo info:', error);
        }
    };

    return {
        photos,
        currentPage,
        totalPages,
        perPage,
        totalPhotos,
        error,
        fetchPhotos,
        fetchThumbnail,
        getPhotoInfo,
    };
}