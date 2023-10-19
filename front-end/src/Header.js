import React from 'react';
import './Header.css'
import mindscape_logo from './mindscape_logo.png'; 

const Header = props => {
  return (
    <div className="header-container">
      <div className="logo-title-container">
        <h1 className="title">MINDSCAPE</h1>
        <img src={mindscape_logo} alt="MINDSCAPE logo" className="logo" />
      </div>
    </div>
  )
}



export default Header;
