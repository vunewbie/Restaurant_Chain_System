import { useState, useEffect } from "react";
import styles from "./Scroller.module.css";

const Scroller = () => {
  const [isVisible, setIsVisible] = useState(false);

  // Kiểm tra vị trí cuộn của trang và ẩn/hiện nút ScrollToTop
  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener("scroll", toggleVisibility);

    // Clean up event listener khi component bị unmount
    return () => {
      window.removeEventListener("scroll", toggleVisibility);
    };
  }, []);

  // Cuộn trang về đầu khi nhấn nút
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <>
      {isVisible && (
        <button
          className={`${styles.scrollToTopBtn} ${isVisible ? styles.visible : ""}`}
          onClick={scrollToTop}
          aria-label="Scroll to top"
        >
          ↑
        </button>
      )}
    </>
  );
};

export default Scroller;
