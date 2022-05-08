import React from "react";
import { useNavigate } from 'react-router-dom';


function NoMatch() {
    const navigate = useNavigate();

    return (
        <div style={{marginLeft:'10px'}}>
        <h2>404Page</h2>
        <h3>you dont need to be here get out</h3>
        <p>Redirecting to <span style={{color:'dodgerblue', cursor:'pointer'}} onClick={() => navigate('/')()}>Login Page</span></p>
        </div>
    );
  }


export default NoMatch;