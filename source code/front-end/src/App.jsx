import React from 'react';
import { Route, Routes } from "react-router-dom";
import {useState, useRef, useEffect, useContext} from "react";
import {Link, useLocation} from "react-router-dom";

import Header from './components/header/Header';
import Footer from './components/footer/Footer';
import Home from "./pages/home/Home";
import About from "./pages/about/About";
import Menu from "./pages/menu/Menu";
import Booking from "./pages/booking/Booking";
import Shipping from "./pages/shipping/Shipping";
import Promotion from "./pages/promotion/Promotion";
import Review from "./pages/review/Review";
import LoginRegister from "./pages/auth/login-register/LoginRegister";
import Scroller from './components/scroller/Scroller';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    () => localStorage.getItem("isLoggedIn") === "true"
  );

  return (

    <>
      <Scroller />
      <Header isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/booking" element={<Booking />} />
        <Route path="/shipping" element={<Shipping />} />
        <Route path="/promotion" element={<Promotion />} />
        <Route path="/review" element={<Review />} />
        <Route path="/login-register" element={<LoginRegister />} />
      </Routes>
      <Footer />
    </>
  );
}

export default App;
