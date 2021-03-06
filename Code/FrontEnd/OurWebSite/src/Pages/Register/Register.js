import React from "react";
import { withRouter } from "../../Components/Navigate";
import "../Register/Register.css"
import axios from 'axios'
import {useNavigate} from "react-router-dom"; 

const USER_REGEX = /^[A-z][A-z0-9-_]{3,23}$/;
const PWD_REGEX = /^(?=.[a-z])(?=.[A-Z])(?=.[0-9])(?=.[!@#$%]).{8,24}$/;
const REGISTER_URL = '/register';

class Register extends React.Component{
    state ={
        userName:'',
        email:'',
        pwd:'',
        register:false,
        errMsg:''
        
    }
    handleChange = (e) =>{
        const {name,value} = e.target
        this.setState({[name]:value})
    }
    handleSubmit = async (e) =>{
        e.preventDefault()
        const signUp = {
            username: this.state.userName,
            password: this.state.pwd,
            id: this.props.myId
        }
        try{
        const response = await axios.post("http://127.0.0.1:8000/guests/register",signUp)
        this.setState({register:true})
        //this.props.handleLog(true);
        //localStorage.setItem("logged","true")
        console.log(response)
        this.setState({errMsg:""}) 
            
        } catch (err){
            console.log(err.response);
            this.setState({errMsg:err.response.data['detail']}) 
        }        
    }
    render(){
        if(!this.state.register)
        return (
            <div className="div-register">
                    <button type="button" className="buttonS" onClick={() => this.props.navigate("/")} style={{ cursor:'pointer', position: 'fixed',width: 50, right: '10px', top: '5px'}}>Back</button>
            <div>
                <form onSubmit = {this.handleSubmit}>
                    <p style={{textAlign: "center"}}>Enter your email and password</p>
                    {this.state.errMsg !== "" ?<p style={{textAlign:'center', color:'red'}} >{this.state.errMsg}</p> : <br />}
                    <input type = 'text' name = 'userName' placeholder="username..." required onChange = {this.handleChange}/>
                    <input type = 'password' name ='pwd' placeholder="password..." required onChange = {this.handleChange}/>
                    <button className="buttonS" style={{backgroundColor:'rgb(161, 28, 28)'}} onSubmit = {this.handleSubmit}>Register</button>
                </form>
            </div>
        </div>
        )
        else{
            return(
                <div className="div-register">
                    <h1 style={{textAlign:"center"}}>Registration complete :)</h1>
                    <p style={{textAlign:"center"}}>sign in <span style={{color:'dodgerblue', cursor:'pointer'}} onClick={() => this.props.navigate('/')}>Here</span></p>
                </div>
                )
        }
        }
}

export default withRouter(Register);