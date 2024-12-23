<script>
// 定义一个全局变量 config，用来存放一些配置信息
var config = {
    API_BASE_URL: 'http://localhost:5000'
};

new Vue({
    el: '#app',
    data: {
        title: 'Image Gallery',
        subtitle: 'Browse and download images',
        photos: [],
        currentPage: 1,
        perPage: 10,
        currentImage: null,
        currentIndex: 0, // 当前图片的索引
        imageModalVisible: false,
        hoveredPhotoId: null,  // 用于控制悬停的图片
        isNightMode: false, // 默认白天模式
    },

    mounted() {
        this.fetchPhotos();  // 初次加载图片列表
        // 设置 favicon
        const link = document.createElement('link');
        link.rel = 'icon';
        link.href = 'img/favicon.ico';  // 从 img 文件夹中加载 favicon
        document.head.appendChild(link);
        window.addEventListener('keydown', this.handleKeydown); // 监听键盘事件
    },
    beforeDestroy() {
        window.removeEventListener('keydown', this.handleKeydown); // 移除事件监听
    },
    computed: {
        // 图片的尺寸随着图片数量变化
        imageStyle() {
            const totalImages = this.photos.length;
            const baseSize = 250; // 基本图片尺寸
            let scale = 1;

            if (totalImages <= 5) {
                scale = 1.2;  // 少图片时放大
            } else if (totalImages > 15) {
                scale = 0.8;  // 多图片时缩小
            }

            return {
                width: `${baseSize * scale}px`,
                height: `auto`,
            };
        },
    },
    methods: {
        // 获取图片列表
        fetchPhotos(page = 1, perPage = 10) {
            axios.get(`${config.API_BASE_URL}/api/photos_list`)
                .then(response => {
                    if (response.data.code === 200) {
                        this.photos = response.data.data.photos;
                    } else {
                        alert('Failed to load photos');
                    }
                })
                .catch(error => {
                    console.error('Error fetching photos:', error);
                });
        },

        // 获取单张图片的公开信息
        getPhotoInfo(photoid) {
            axios.get(`${config.API_BASE_URL}/api/getphotoinfo?photoid=${photoid}&thumbnail=1`)
                .then(response => {
                    if (response.data.code === 200) {
                        this.currentImage = response.data.data;
                        this.imageModalVisible = true;
                        this.$nextTick(() => {
                            // 为放大后的图片添加 zoomed 类
                            document.querySelector('.modal-image').classList.add('zoomed');
                        });
                    } else {
                        alert('Failed to load photo info');
                    }
                })
                .catch(error => {
                    console.error('Error fetching photo info:', error);
                });
        },

        // 下载图片
        downloadImage(photoid) {
            const photo = this.photos.find(p => p.photoid === photoid);
            const downloadUrl = `${config.API_BASE_URL}/api/getphoto?photoid=${photoid}&thumbnail=1`;
            window.location.href = downloadUrl;
        },

        // 关闭模态框
        closeModal() {
            this.imageModalVisible = false;
            document.querySelector('.modal-image').classList.remove('zoomed');
        },
        // 切换到上一张
        prevImage() {
            if (this.currentIndex > 0) {
              console.log(this.currentIndex,"->",this.currentIndex - 1);
                this.getPhotoInfo(this.photos[this.currentIndex - 1].photoid, this.currentIndex - 1);
            }
        },

        // 切换到下一张
        nextImage() {
            if (this.currentIndex < this.photos.length - 1) {
              console.log(this.currentIndex,"->",this.currentIndex + 1," len:",this.photos.length);
                this.getPhotoInfo(this.photos[this.currentIndex + 1].photoid, this.currentIndex + 1);
            }
        },

        // 处理键盘方向键事件
        handleKeydown(event) {
            if (this.imageModalVisible) {
                if (event.key === 'ArrowLeft') {
                    this.prevImage(); // 左箭头切换到上一张
                } else if (event.key === 'ArrowRight') {
                    this.nextImage(); // 右箭头切换到下一张
                }
            }
        },
        // 图片点击放大，切换图片
        toggleImageSize() {
            this.imageModalVisible = !this.imageModalVisible;
        },

        // 鼠标悬停在图片上时
        hoverImage(photoid) {
            this.hoveredPhotoId = photoid;
        },

        // 判断图片是否被悬停
        isHovered(photoid) {
            return this.hoveredPhotoId === photoid;
        },
        // 切换白天/夜间模式
        toggleMode() {
            this.isNightMode = !this.isNightMode;
            // 添加或移除 night-mode 类
            if (this.isNightMode) {
                document.body.classList.add('night-mode');
            } else {
                document.body.classList.remove('night-mode');
            }
        },
    },
    template: `
    <div class="container">
      <header class="header">
        <h1>{{ title }}</h1>
        <h2>{{ subtitle }}</h2>
        <!-- 白天/夜间模式按钮 -->
        <button class="mode-toggle-btn" @click="toggleMode">🌙</button>
      </header>

      <!-- 图片展示区域 -->
      <div class="image-gallery">
        <div 
          v-for="photo in photos" 
          :key="photo.photoid" 
          class="image-card" 
          @mouseover="hoverImage(photo.photoid)" 
          @mouseleave="hoverImage(photo.photoid)"
          :style="imageStyle"
          @click="getPhotoInfo(photo.photoid)"
        >
          <img :src="photo.thumbnail" :alt="photo.desc">
          <div class="overlay">
            <div class="overlay-content">
              <p>{{ photo.upload_user }}</p>
              <p>{{ photo.upload_time }}</p>
              <p>{{ photo.desc }}</p>
              <button 
                @click.stop="downloadImage(photo.photoid)" 
                :style="isHovered(photo.photoid) ? { transform: 'scale(0.8)' } : {}"
              >
                下载原图
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 图片查看模态框 -->
      <div v-if="imageModalVisible" class="image-modal" @click="toggleImageSize">
        <div class="modal-content">
          <span @click="closeModal" class="close-btn">×</span>
                    <!-- 左右切换按钮 -->
          <button class="prev-btn" @click="prevImage">&lt;</button>
          <button class="next-btn" @click="nextImage">&gt;</button>
          <img :src="currentImage ? currentImage.thumbnail : ''" alt="Current Image" class="modal-image">
          <div class="image-info">
            <p>{{ currentImage ? currentImage.name : '' }}</p>
            <p>{{ currentImage ? currentImage.desc : '' }}</p>
            <p>{{ currentImage ? currentImage.upload_time : '' }}</p>
            <p>{{ currentImage ? currentImage.uploader : '' }}</p>
          </div>
        </div>
      </div>
    </div>
  `,
});

</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;  /* 白天背景 */
  color: #33333373;  /* 白天文字颜色 */
  transition: background-color 0.3s ease, color 0.3s ease; /* 添加过渡动画 */
}

/* 夜间模式样式 */
body.night-mode {
  background-color: #2c2c2c;  /* 夜间背景 */
  color: #96fff6;  /* 夜间文字颜色 */
  transition: background-color 0.3s ease, color 0.3s ease; /* 添加过渡动画 */
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

/* 夜间模式下的文字颜色 */
body.night-mode .header h1 {
  color: #ddd !important;
}

body.night-mode .header h2 {
  color: #fff !important;
}


/* 切换按钮样式 */
.mode-toggle-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 10px 10px;
  background-color: #2fe4eb81;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s;
}

.mode-toggle-btn:hover {
  background-color: #3e86f157;
}
/* 页面背景 */
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('img/background.png') no-repeat center center/cover;
  z-index: -1;
  filter: blur(8px);  /* 背景模糊效果 */
}

/* Container */
.container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 10px;
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 36px;
  color: #333;
}

.header h2 {
  font-size: 18px;
  color: #555;
}

/* 图片展示区域 */
.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

/* 图片卡片 */
.image-card {
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease;
}

/* 鼠标悬浮时图片轻微放大 */
.image-card:hover {
  transform: scale(1.05);
}

.image-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

/* Hover Overlay */
.image-card .overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 8px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 显示图片信息 */
.image-card .overlay-content {
  text-align: center;
  padding: 10px;
}

/* 鼠标悬浮时显示 overlay */
.image-card:hover .overlay {
  opacity: 1;
}

/* 下载按钮 */
button {
  background-color: #ff6600;
  border: none;
  color: white;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s ease;
  transform: scale(1);
}

button:hover {
  background-color: #e65c00;
}

/* 图片查看模态框 */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  backdrop-filter: blur(5px); /* 背景模糊 */
}

/* Modal 内容 */
.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 90%;
  max-height: 80%;
  overflow-y: auto;
}

/* 图片查看模态框 */
.modal-image {
  max-width: 100%;
  height: auto;
  transition: transform 0.3s ease;
}

/* 图片信息 */
.image-info {
  margin-top: 20px;
  text-align: center;
}

/* 关闭按钮 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 30px;
  cursor: pointer;
  color: #000;
}

/* 磨砂背景 */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7); /* 背景暗化 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  backdrop-filter: blur(5px); /* 使用 backdrop-filter 添加磨砂效果 */
}
/* 关闭按钮 */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 30px;
  cursor: pointer;
  color: #000;
}

/* 图片查看模态框 */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7); /* 背景暗化 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  backdrop-filter: blur(5px); /* 使用 backdrop-filter 添加磨砂效果 */
}

/* 模态框内的内容 */
.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 90%;
  max-height: 80%;
  overflow-y: auto;
  position: relative;
}

/* 图片 */
.modal-image {
  max-width: 100%;
  height: auto;
  transition: transform 0.3s ease; /* 添加平滑过渡 */
}


/* 左右切换按钮 */
.prev-btn, .next-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 20px;
  z-index: 1000;
}

.prev-btn {
  left: 10px;
}

.next-btn {
  right: 10px;
}

.prev-btn:hover, .next-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

/* 鼠标悬停图片时放大一点，移除放大后的 hover 效果 */
.modal-image:not(.zoomed):hover {
  transform: scale(1.05); /* 放大效果 */
}

/* 通过添加 .zoomed 类来禁用 hover 放大效果 */
.modal-image.zoomed {
  transform: scale(1); /* 已经放大的图片不应用 hover 效果 */
}
</style>