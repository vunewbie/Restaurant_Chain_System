import React, { useState, useRef, useEffect } from "react";
import { Link, NavLink, useNavigate, useLocation } from "react-router-dom";
import styles from "./Header.module.css";
import logo from "../../assets/logo.jpg";

const Header = ({ isLoggedIn, setIsLoggedIn }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();
  const horiSelectorRef = useRef(null);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.setItem("isLoggedIn", "false");
    navigate("/");
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const navItems = document.querySelectorAll(`.${styles.navItem}`);
    let activeItem = null;
    
    navItems.forEach((item) => {
      const link = item.querySelector("a");
      if (link && link.getAttribute("href") === location.pathname) {
        item.classList.add(styles.active);
        activeItem = item;
      } else {
        item.classList.remove(styles.active);
      }
    });
  
    if (activeItem && horiSelectorRef.current) {
      const { offsetLeft, offsetWidth, offsetHeight } = activeItem;
      horiSelectorRef.current.style.left = `${offsetLeft}px`;
      horiSelectorRef.current.style.width = `${offsetWidth}px`;
      horiSelectorRef.current.style.height = `${offsetHeight}px`;
    }
  }, [location]);
  

  return (
    <nav className={`${styles.navbar} navbar-expand-custom ${styles.navbarMainbg}`}>
      <Link to="/" className={`${styles.navbarLogo}`}>
        <img src={logo} alt="Logo" className={styles.logo} />
      </Link>
      <button className={styles.navbarToggler} onClick={toggleMenu}>
        <i className="fas fa-bars text-white"></i>
      </button>
      <div className={`collapse navbar-collapse ${isMenuOpen ? styles.showMenu : ""}`}>
        <ul className={`${styles.navbarNav} ml-auto`}>
          <div className={styles.horiSelector} ref={horiSelectorRef}></div>
          <li className={styles.navItem}><NavLink to="/" className={styles.navLink}>Trang chủ</NavLink></li>
          <li className={styles.navItem}><NavLink to="/about" className={styles.navLink}>Giới thiệu</NavLink></li>
          <li className={styles.navItem}><NavLink to="/menu" className={styles.navLink}>Thực đơn</NavLink></li>
          <li className={styles.navItem}><NavLink to="/booking" className={styles.navLink}>Đặt bàn</NavLink></li>
          <li className={styles.navItem}><NavLink to="/shipping" className={styles.navLink}>Giao hàng</NavLink></li>
          <li className={styles.navItem}><NavLink to="/promotion" className={styles.navLink}>Ưu đãi</NavLink></li>
          <li className={styles.navItem}><NavLink to="/review" className={styles.navLink}>Đánh giá</NavLink></li>
          
          {isLoggedIn ? (
            <li className={styles.navItem} ref={menuRef}>
              <button onClick={toggleDropdown} className={styles.navLink}>
                <img src={logo} alt="Avatar" className={styles.avatar} /> Tài khoản
              </button>
              {isDropdownOpen && (
                <ul className={styles.dropdownMenu}>
                  <li><NavLink to="/account" className={styles.dropdownItem}>Quản lý</NavLink></li>
                  <li><button onClick={handleLogout} className={styles.dropdownItem}>Đăng xuất</button></li>
                </ul>
              )}
            </li>
          ) : (
            <li className={styles.navItem}><NavLink to="/login-register" className={styles.navLink}>Đăng nhập</NavLink></li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Header;
