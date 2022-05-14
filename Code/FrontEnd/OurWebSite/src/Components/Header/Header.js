import React from "react";
import { NavLink ,useLocation,useNavigate,useParams} from "react-router-dom"; 
import {ReactComponent as LogoIcon} from '../../Assets/ricardo.svg'
import {ReactComponent as MyStoreIcon} from '../../Assets/myStore.svg'
import {ReactComponent as SearchIcon} from '../../Assets/search.svg'
import {ReactComponent as CartIcon} from '../../Assets/shopping_cart.svg'
import {ReactComponent as MyAccountIcon} from '../../Assets/myaccount-icon.svg'
import './Header.css';
import axios from 'axios'


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

function Header({handleLogin, checkLogged }){
    const navigate = useNavigate();

    const logout = async ()=>{
      if (checkLogged){
        try{
        const response = await axios.post('http://127.0.0.1:8000/users/logout')
        console.log(response)
        handleLogin(false)
        localStorage.setItem("logged","false")
        navigate('/')
        } catch (err){
            console.log(err.response);
        }
      }
      else{
        navigate('/')
      }
    }
    return(
        <nav>
            <div className="div-header">
                <div >
                    <LogoIcon onClick={() => navigate('/home')} style={{cursor:'pointer'}} className="logo"/> 
                    <NavLink to ='/home/my-account'activeclassname='active'><MyAccountIcon 
                    style={{height: '40px',width: '40px',padding: '0 20px'}}/></NavLink>

                </div>
                <div style={{display:'flex',flexDirection:'row',alignItems:'center'}}>
                    <NavLink to ='/home/MyStores' activeclassname='active'><MyStoreIcon className="div-svg"/></NavLink>
                    <NavLink to ='/home/explore'activeclassname='active'><SearchIcon className="div-svg"/></NavLink>
                    <NavLink to ='/home/shopping-cart'activeclassname='active'><CartIcon className="div-svg"/></NavLink>


                    <button className="button-header" onClick={logout} style={{ cursor:'pointer'}}>{formatExit(checkLogged)}</button>
                </div>
            </div>
        </nav>
        
    )
}

function formatExit(isLogged){
  return isLogged ? 'Log out' : 'Exit'

}

export default withRouter(Header);