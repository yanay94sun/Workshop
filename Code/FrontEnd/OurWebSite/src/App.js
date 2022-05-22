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

  const [userId, setUserId] = useState("")

  useEffect(() => {
    hendleEntrec();
  }, []);

  const hendleEntrec = async () =>{
      localStorage.setItem("user_id","fsdf")
      localStorage.setItem("logged","false")
      const checkIfLogged = localStorage.getItem("logged")
      if (checkIfLogged){
        if (checkIfLogged === "true"){
          setIsLog(true)
        }
        else{
          setIsLog(false)
        }
      }
      const loggedUser = localStorage.getItem("user_id")
      if (loggedUser && !isNaN(loggedUser)){
          setUserId(loggedUser)
          console.log("id is "+loggedUser)
      }
      else{
      const response = await axios.get('http://127.0.0.1:8000/guests/enter')
      localStorage.setItem("user_id",response.data.value)   
      setUserId(response.data.value)
      console.log(response) 
      }
  }
  return (
    <div>
      <Routes >
        <Route path = '/' element= {<Login setLogin={setIsLog} isLogged = {isLog} myId = {userId}/>}/>
        <Route path = '/home/*' element = {<Home setLogin ={setIsLog}  isLogged = {isLog} myId = {userId}/>}/>
        <Route path ="/register" element= {<Register handleLog = {setIsLog} logged = {isLog} myId = {userId} />}/>
        <Route path = '*' element={<NoMatch/>}/>
      </Routes>
    </div>
  )
}
export default App;