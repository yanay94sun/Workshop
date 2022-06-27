import React, {Component, useState} from 'react';

function MyAccount(messages){
    const [msgs, setMsgs] = useState(messages);
    const [counter, setCounter] = useState(0);
    
return(
    <div>
        <h2>My Account </h2>
        <ul>
            {msgs.map((message) => (
                <li> {message}</li>
            ))}
        </ul>
    </div>
)
}

export default MyAccount;
