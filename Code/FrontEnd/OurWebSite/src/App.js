import React, {useState, useEffect} from "react";
import {Routes , Route} from 'react-router-dom';
import NoMatch from "./Pages/404Page/404Page";
import Home from "./Pages/Home/Home";
import Login from "./Pages/Login/Login";
import Register from "./Pages/Register/Register.js";
import axios from "axios";


axios.defaults.withCredentials = true

function App() {

  const [isLog,setIsLog] = useState(false)

  useEffect(() => {
    hendleEntrec();
   // setIsLog(isLogFromServer());
  }, []);

  const isLogFromServer = async () =>{
    //const response = await ...
    return true // or false 
  }

  const hendleEntrec = async () =>{
      const response = await axios.get('http://127.0.0.1:8000/guests/enter')
      console.log(response)    
  }
  return (
    <div>
      <Routes >
        <Route path = '/' element= {<Login setLogin={setIsLog} />}/>
        <Route path = '/home/*' element = {<Home setLogin ={setIsLog}  isLogged = {isLog}/>}/>
        <Route path ="/register" element= {<Register handleLog = {setIsLog} logged = {isLog} />}/>
        <Route path = '*' element={<NoMatch/>}/>
      </Routes>
    </div>
  )
}
export default App;