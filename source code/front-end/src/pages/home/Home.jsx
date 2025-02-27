import React, { useState, useEffect } from "react";
import styles from "./Home.module.css";

// Hàm import ảnh từ thư mục (Lấy giá trị default)
const importImages = (context) => {
  return Object.values(context).map((module) => module.default);
};

// Import ảnh từ các thư mục cố định
const introImages = importImages(
  import.meta.glob("../../assets/home/intro/*.{png,jpg,jpeg,svg}", { eager: true })
);
const hcmImages = importImages(
  import.meta.glob("../../assets/home/hcm/*.{png,jpg,jpeg,svg}", { eager: true })
);
const hnImages = importImages(
  import.meta.glob("../../assets/home/hn/*.{png,jpg,jpeg,svg}", { eager: true })
);
const dnImages = importImages(
  import.meta.glob("../../assets/home/dn/*.{png,jpg,jpeg,svg}", { eager: true })
);

const Home = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedImage, setSelectedImage] = useState(null);

  const hcmTitles = [
    "Kyo Sushi Quận 8", "Lá Phong Sushi House Quận 1", "Sorae Sushi Quận 1",
    "Sushi Tei Quận 3", "Sushiway Thủ Đức", "Takashi Sushi Bình Chánh",
    "Taki Sushi Thủ Đức", "Yen Sushi & Sake Pub Quận 3"
  ];
  
  const hnTitles = [
    "Hadu Sushi Đống Đa", "Kiraku Japanese Restaurant Hai Bà Trưng", "Sushi Bar Xuân Diệu",
    "Sushi Kei Long Biên", "Sushi Lab Hoàn Kiếm", "Tokyo Deli Hoàng Đạo Thụy",
    "Tuski Sushi Hoàng Mai", "Trạm Sushi Ba Đình"
  ];
  
  const dnTitles = [
    "Akataiyo Sushi Hai Châu", "Chen Sushi Cẩm Lệ", "Dasushi Thanh Khê",
    "Issun Boshi Ngũ Hành Sơn", "Kyoto Sushi Japanese Sơn Trà", "Little Tokyo Ngũ Hành Sơn",
    "Mogu Mogu Cẩm Lệ", "Sushi Time Thanh Khê"
  ];

  // Tự động chuyển ảnh sau 3 giây
  useEffect(() => {
    const interval = setInterval(() => {
      goToNextSlide();
    }, 3000);
    return () => clearInterval(interval);
  }, [currentIndex]);

  // Chuyển đến slide tiếp theo
  const goToNextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % introImages.length);
  };

  // Chuyển đến slide trước đó
  const goToPrevSlide = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === 0 ? introImages.length - 1 : prevIndex - 1
    );
  };

  return (
    <div className={styles.homeContainer}>
      {/* ==== Slider ==== */}
      <div className={styles.sliderContainer}>
        <div className={styles.slider}>
          {introImages.map((img, index) => (
            <img
              key={index}
              src={img}
              alt={`Slide ${index + 1}`}
              className={`${styles.slide} ${index === currentIndex ? styles.active : ""}`}
            />
          ))}
        </div>

        {/* Nút điều hướng trái & phải */}
        <button className={styles.prevButton} onClick={goToPrevSlide}>
          ❮
        </button>
        <button className={styles.nextButton} onClick={goToNextSlide}>
          ❯
        </button>
      </div>

      {/* ==== Ba phần: Hồ Chí Minh - Hà Nội - Đà Nẵng ==== */}
      {[
        { title: "Hồ Chí Minh", images: hcmImages, titles: hcmTitles },
        { title: "Hà Nội", images: hnImages, titles: hnTitles },
        { title: "Đà Nẵng", images: dnImages, titles: dnTitles },
      ].map((section, idx) => (
        <div key={idx} className={styles.section}>
          <h1 className={styles.sectionTitle}>{section.title}</h1>
          <div className={styles.imageGallery}>
            {section.images.map((img, index) => (
              <div
                key={index}
                className={styles.imageWrapper}
                onClick={() => setSelectedImage(img)}
              >
                <img src={img} alt={`${section.titles[index]}`} className={styles.galleryImage} />
                <div className={styles.imageOverlay}>
                  <span className={styles.imageText}>{section.titles[index]}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Lightbox khi ảnh được click */}
      {selectedImage && (
        <div className={styles.lightbox} onClick={() => setSelectedImage(null)}>
          <img src={selectedImage} alt="Phóng to" className={styles.lightboxImage} />
        </div>
      )}
    </div>
  );
};

export default Home;
