import React  from "react";
import { useState, useEffect } from 'react';
import { NavLink ,useLocation,useNavigate,useParams} from "react-router-dom"; 
import {ReactComponent as LogoIcon} from '../../Assets/ricardo.svg'
import {ReactComponent as MyStoreIcon} from '../../Assets/myStore.svg'
import {ReactComponent as SearchIcon} from '../../Assets/search.svg'
import {ReactComponent as CartIcon} from '../../Assets/shopping_cart.svg'
import {ReactComponent as MyAccountIcon} from '../../Assets/myaccount-icon.svg'
import {ReactComponent as AdminLogo} from '../../Assets/admin.svg'

import {ReactComponent as MyAccountNotifIcon} from '../../Assets/icons8-add-male-user-64.svg'
import './Header.css';
import axios from 'axios'
// import io from "socket.io-client";
import Popup from "reactjs-popup";


// const socket = io.connect("http://127.0.0.1:8000");

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
    // var ws =  null;
    const navigate = useNavigate();
    const [hasNotification, setHasNotification] = useState(false);
    const [isAdmin, setIsAadmin] = useState(false)
    const [messages, setMessages] = useState([]);

    const logout = async ()=>{
      const ID = {
        id: localStorage.getItem('user_id')
      }
      if (checkLogged){
        try{
        const response = await axios.post('http://127.0.0.1:8000/users/logout',ID)
        console.log(response)
        handleLogin(false)
        localStorage.setItem("logged","false")
        navigate('/')
        } catch (err){
            console.log(err.response);
        }
      }
      else{
        try{
           const response = await axios.post('http://127.0.0.1:8000/exit',ID);
          console.log(response)
          navigate('/')
        } catch (err){
          console.log(err.response);
        }
      }
    }

    const handleMyAccount = () => {
        setHasNotification(false);
    }

    const checkAdmin = async () => {
      try{
        const response = await axios.get('http://127.0.0.1:8000/is_admin/'+localStorage.getItem("user_id"))
        console.log(response)
        setIsAadmin(response.data.value)
      }catch (err){
          console.log(err.response);
        }
    }

    useEffect(() => {
      checkAdmin()
    }, []);

    const handlePullingUserMsg = async () => {
        try{
            const response = await axios.get('http://127.0.0.1:8000/get_user_msgs/'+localStorage.getItem("user_id"))
            console.log(response)
            const msgs = response.data;
            if (msgs.length > 0){
                setMessages(msgs);
                setHasNotification(true);
            }
        }catch (err){
              console.log(err.response);
        }
    }

    useEffect(() => {
        handlePullingUserMsg()
    }, [])

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws');
        ws.onopen = () => {
            ws.send(localStorage.getItem("user_id"));
        }
        ws.onmessage = (e) => {
            console.log("Accepted Message: ", e.data)
            setHasNotification(true);

            // const old_msg = [...messages];
            // old_msg.concat([e.data]);
            // setMessages(old_msg);
            // console.log(messages);

            setMessages([...messages, e.data]);
            console.log(messages);
        }
    }, [messages])
    // useEffect(() => {
    //   socket.on("receive_message", () => {
    //     setHasNotification(true);
    //   });
    // }, [socket]);


    return(
        <nav>
            <div className="div-header">
                <div >
                    <LogoIcon onClick={() => navigate('/home')} style={{cursor:'pointer'}} className="logo"/>
                    {hasNotification ?
                    //     <NavLink onClick={() => handleMyAccount()} to ='/home/my-account' activeclassname='active'><MyAccountNotifIcon
                    // style={{height: '40px',width: '40px',padding: '0 20px'}}/></NavLink> :

                        <Popup onClose={handleMyAccount} trigger={<NavLink  to ='/home/my-account' activeclassname='active'><MyAccountNotifIcon
                            style={{height: '40px',width: '40px',padding: '0 20px'}}/></NavLink>} position="right center">
                            <div>
                                <ul>
                                    {messages.map((message) => (
                                    <li>
                                        {message}
                                    </li>))}

                                </ul>
                            </div>
                        </Popup>
                        :
                    <NavLink to ='/home/my-account' activeclassname='active'><MyAccountIcon
                    style={{height: '40px',width: '40px',padding: '0 20px'}}/></NavLink>
                    }

                </div>
                <div style={{display:'flex',flexDirection:'row',alignItems:'center'}}>
                    {isAdmin ? <NavLink to ='/home/admin' activeclassname='active' className='img__wrap'>
                      <AdminLogo className="div-svg"/>
                    <p className="img__description">admin options</p>
                    </NavLink>: ""}
                    <NavLink to ='/home/MyStores' activeclassname='active' className='img__wrap'>
                      <MyStoreIcon className="div-svg"/>
                    <p className="img__description">My stores</p>
                    </NavLink>
                    <NavLink to ='/home/explore' activeclassname='active' className='img__wrap'>
                      <SearchIcon className="div-svg"/> 
                      <p className="img__description">Search</p>
                    </NavLink>
                    <NavLink to ='/home/shopping-cart' activeclassname='active' className='img__wrap'>
                      <CartIcon className="div-svg"/>
                      <p className="img__description">Shopping cart</p>

                    </NavLink>


                    <button className="buttonS" onClick={logout} style={{ cursor:'pointer'}}>{formatExit(checkLogged)}</button>
                </div>
            </div>
        </nav>
        
    )
}

function formatExit(isLogged){
  return isLogged ? 'Log out' : 'Exit'

}

export default withRouter(Header);