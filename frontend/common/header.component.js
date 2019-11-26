import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom'
import { session } from '../session'

function Header(props) {
  return (
    <header>
      <div>
        <Link to="/"><img className="menuToggle" alt='logo' src="/static/img/vframe_icon_white.svg" /></Link>
        <Link to="/" className="vcat-btn"><b>VFRAME</b></Link>
      </div>
      <div>
        <Link to="/search/">Search</Link>
        <Link to="/collection/">Collections</Link>
        <Link to="/dashboard/">Dashboard</Link>
        <span className='username' onClick={() => changeUsername()}>
          {' → '}{props.username}
        </span>
      </div>
    </header>
  )
}

const changeUsername = () => {
  const username = prompt("Please enter your username:", session('username'))
  if (username && username.length) {
    session.set('username', username)
    document.querySelector('Header div span').innerText = ' → ' + username // very naughty
  }
}


const mapStateToProps = (state) => ({
  auth: state.auth,
  username: session.get('username'),
  isAuthenticated: state.auth.isAuthenticated,
});

const mapDispatchToProps = (dispatch) => ({
});

export default connect(mapStateToProps, mapDispatchToProps)(Header);
