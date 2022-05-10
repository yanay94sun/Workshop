import React from "react";
import {Routes , Route} from 'react-router-dom';
import NoMatch from "./Pages/404Page/404Page";
import Explore from "./Pages/Explore/Explore";
import Home from "./Pages/Home/Home";
import Login from "./Pages/Login/Login";
import NewHome from "./Pages/NewHome/NewHome";
import Register from "./Pages/Register/Register.js";
import axios from "axios";

axios.defaults.withCredentials = true

class App extends React.Component {
  state ={
    isLog:false
  }
  handleLogin = (isLog) => this.setState({isLog})
  
  hendleEntrec = async () =>{
    // connecting to back
    // e.preventDefault();
    const response = await axios.get('http://127.0.0.1:8000/guests/enter')
    console.log(response.data)
  }

  render(){
    const {isLog} = this.state;
    this.hendleEntrec();

  return (
    <div>
      <Routes >
        <Route path = '/' element= {<Login isLogin={this.handleLogin} />}/>
        <Route path = '/home/*' element = {<Home handleLogged={this.handleLogin}/>}/>
        <Route path ="/register" element= {<Register/>}/>
        <Route path = '*' element={<NoMatch/>}/>
      </Routes>
    </div>
  )
  }
}
export default App;
