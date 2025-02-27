import React from "react";
import { FaFacebook, FaTiktok, FaFacebookMessenger, FaYoutube } from "react-icons/fa";
import styles from "./Footer.module.css";

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContainer}>
        {/* Cột 1: Bản đồ */}
        <div className={styles.footerColumn}>
          <h3>Bản đồ</h3>
          <iframe
            src="https://www.google.com/maps?q=447+QL13,+Lộc+Ninh,+Bình+Phước,+Việt+Nam&output=embed"
            width="100%"
            height="200"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
          ></iframe>
        </div>

        {/* Cột 2: Thông tin công ty (Căn lề trái) */}
        <div className={`${styles.footerColumn} ${styles.textLeft}`}>
          <h3>CÔNG TY TNHH MTV VUNEWBIE</h3>
          <p><strong>Mã Số Thuế:</strong> 8883898250</p>
          <p><strong>Người Đại Diện:</strong> Nguyễn Hoàng Vũ</p>
          <p><strong>Địa Chỉ:</strong> 447, Quốc lộ 13, Khu phố Ninh Thái, Thị trấn Lộc Ninh, Huyện Lộc Ninh, Tỉnh Bình Phước</p>
          <p><strong>Hotline:</strong> 0386323603</p>
        </div>

        {/* Cột 3: Điều khoản (Căn lề trái) */}
        <div className={`${styles.footerColumn} ${styles.textLeft}`}>
          <h3>THÔNG TIN ĐIỀU KHOẢN</h3>
          <ul>
            <li><a href="#">Điều khoản sử dụng</a></li>
            <li><a href="#">Chính sách bảo mật</a></li>
            <li><a href="#">Chính sách thẻ thành viên</a></li>
          </ul>
        </div>

        {/* Cột 4: Mạng xã hội */}
        <div className={styles.footerColumn}>
          <h3>MẠNG XÃ HỘI</h3>
          <ul className={styles.socialLinks}>
            <li>
              <a href="https://www.facebook.com/vu.nguyen.hoang.86543" target="_blank" rel="noopener noreferrer">
                <FaFacebook size={24} color="#1877F2" />
              </a>
            </li>
            <li>
              <a href="https://www.tiktok.com/@sapthatnghiephuhu" target="_blank" rel="noopener noreferrer">
                <FaTiktok size={24} color="#000" />
              </a>
            </li>
            <li>
              <a href="https://m.me/vu.nguyen.hoang.86543" target="_blank" rel="noopener noreferrer">
                <FaFacebookMessenger size={24} color="#0084FF" />
              </a>
            </li>
            <li>
              <a href="https://www.youtube.com/@vunguyenhoang7831" target="_blank" rel="noopener noreferrer">
                <FaYoutube size={24} color="#FF0000" />
              </a>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
