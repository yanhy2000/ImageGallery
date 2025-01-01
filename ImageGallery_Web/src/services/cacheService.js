// src/services/cacheService.js
export const openDatabase = () => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('PhotoCacheDB', 1);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('photos')) {
        const store = db.createObjectStore('photos', { keyPath: 'id' });
        store.createIndex('timestamp', 'timestamp', { unique: false }); 
      }
    };

    request.onsuccess = (event) => resolve(event.target.result);
    request.onerror = (event) => reject(event.target.error);
  });
};

export const cachePhoto = async (photoId, thumbnailUrl, thumbnailBlob) => {
  const db = await openDatabase();
  const transaction = db.transaction('photos', 'readwrite');
  const store = transaction.objectStore('photos');
  const timestamp = Date.now();
  store.put({ id: photoId, thumbnailUrl, blob: thumbnailBlob, timestamp });
  console.log(`Photo ${photoId} cached with binary data.`);
};

export const getCachedPhoto = async (photoId) => {
  const db = await openDatabase();
  const transaction = db.transaction('photos', 'readonly');
  const store = transaction.objectStore('photos');

  return new Promise((resolve, reject) => {
    const request = store.get(photoId);
    request.onsuccess = () => {
      const result = request.result;

      if (result) {
        resolve(result);
      } else {
        resolve(null);
      }
    };
    request.onerror = (error) => reject(error);
  });
};

export const cleanExpiredPhotos = async (expiryTime = 7 * 24 * 60 * 60 * 1000) => { 
  const db = await openDatabase();
  const transaction = db.transaction('photos', 'readwrite');
  const store = transaction.objectStore('photos');
  const now = Date.now();

  store.openCursor().onsuccess = (event) => {
    const cursor = event.target.result;
    if (cursor) {
      const photo = cursor.value;
      if (now - photo.timestamp > expiryTime) {
        store.delete(photo.id);
        console.log(`Photo ${photo.id} expired and removed from cache.`);
      }
      cursor.continue();
    }
  };
  await cleanCacheSize(store, 500 * 1024 * 1024); // 限制总大小为 500MB
};

const cleanCacheSize = async (store, maxCacheSize) => {
  const photoSizes = [];
  let totalSize = 0;

  return new Promise((resolve) => {
    store.openCursor().onsuccess = (event) => {
      const cursor = event.target.result;
      if (cursor) {
        const photo = cursor.value;
        const blobSize = photo.blob.size || 0; 
        photoSizes.push({ id: photo.id, size: blobSize, timestamp: photo.timestamp });
        totalSize += blobSize;
        cursor.continue();
      } else {
        if (totalSize > maxCacheSize) {
          console.log(`Cache size exceeds ${maxCacheSize} bytes. Cleaning oldest entries.`);
          photoSizes.sort((a, b) => a.timestamp - b.timestamp); 
          const itemsToDelete = photoSizes.slice(0, 10); 
          for (const item of itemsToDelete) {
            store.delete(item.id);
            console.log(`Deleted photo ${item.id} to free up space.`);
          }
        }
        resolve();
      }
    };
  });
};

export const refreshCache = async () => {
  const db = await openDatabase();
  const transaction = db.transaction('photos', 'readwrite');
  const store = transaction.objectStore('photos');
  store.clear();
  console.log('IndexedDB cache cleared.');
  if ('caches' in window) {
    caches.keys().then((cacheNames) => {
      cacheNames.forEach((cacheName) => {
        caches.delete(cacheName);
      });
    });
  }
  console.log('Browser cache cleared.');
  window.location.reload();
};
