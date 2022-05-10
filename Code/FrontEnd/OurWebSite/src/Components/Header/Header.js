import React from "react";
import { NavLink ,useLocation,useNavigate,useParams} from "react-router-dom"; 
import {ReactComponent as LogoIcon} from '../../Assets/ricardo.svg'
import {ReactComponent as HomeIcon} from '../../Assets/home.svg'
import {ReactComponent as ExploreIcon} from '../../Assets/explore.svg'
import {ReactComponent as CartIcon} from '../../Assets/shopping_cart.svg'
import {ReactComponent as MyAccountIcon} from '../../Assets/myaccount-icon.svg'
import './Header.css';

function withRouter(Component) {
    function ComponentWithRouterProp(props) {
      let location = useLocation();
      let navigate = useNavigate();
      let params = useParams();
      return (
        <Component
          {...props}
          router={{ location, navigate, params }}
        />
      );
    }
  
    return ComponentWithRouterProp;
  }

function Header({isLogged}){
    const navigate = useNavigate();
    const handleClick = ()=>{
        navigate('/')
        isLogged(false)
    }
    return(
        <nav>
            <div className="div-header">
                <div >
                    <LogoIcon onClick={() => navigate('/home')()} style={{cursor:'pointer'}} className="logo"/> 
                </div>
                <div style={{display:'flex',flexDirection:'row',alignItems:'center'}}>
                    <NavLink to ='/home/newHome' activeClassName='active'><HomeIcon className="div-svg"/></NavLink>
                    <NavLink to ='/home/explore'activeClassName='active'><ExploreIcon className="div-svg"/></NavLink>
                    <NavLink to ='/home/shopping-cart'activeClassName='active'><CartIcon className="div-svg"/></NavLink>
                    <NavLink to ='/home/my-account'activeClassName='active'><MyAccountIcon className="div-svg"/></NavLink>


                    <button className="button-header" onClick={handleClick} style={{ cursor:'pointer'}}>log out</button>
                </div>
            </div>
        </nav>
        
    )
}

function formatExit(){
  return this.props.isLogged ? 'Log out' : 'Exit'

}

export default withRouter(Header);