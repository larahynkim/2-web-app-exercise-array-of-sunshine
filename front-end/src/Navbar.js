import './Navbar.css'
import { Link } from 'react-router-dom'
import home_icon from './home_icon.png' // import the home icon
import journal_icon from './journal_icon.png' // import the journal icon
import calendar_icon from './calendar_icon.png' // import the calendar icon

const Navbar = props => {
  return (
    <div className="navbar-wrapper">
      <aside className="side-navbar">
        <div className="nav-links">
          <Link to="/" className="nav-item">
            <img src={home_icon} alt="Home" />
          </Link>
          <Link to="/journal" className="nav-item">
            <img src={journal_icon} alt="Journal" />
          </Link>
          <Link to="/calendar" className="nav-item"> 
            <img src={calendar_icon} alt="Calendar" />
          </Link>
        </div>
      </aside>
    </div>
  )
}

export default Navbar
