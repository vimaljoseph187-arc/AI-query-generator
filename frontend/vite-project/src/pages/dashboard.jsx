import { useState, useEffect } from "react"
import API from "../config"
import axios from "axios";

function Dashboard(){
    const [data,setUser]=useState([])

    useEffect (()=>{
        axios.get(`${API.BASE_URL}/api/get/all_users`)
        .then((res) => {
            console.log("API Response:", res.data);
            const users =res.data.data || (Array.isArray(res.data) ? res.data : []);
            setUser(users);
          })
          .catch((err) => {
            console.log(err);
            setUser([]);
          })
    },[])


    return (
        <>
        <table>
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Password Hash</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
                {
                !Array.isArray(data) || data.length === 0 ?
                (
                    <tr>
                    <td colSpan="3">No Record</td>
                  </tr>

                )
                : (
                    data.map((user) => (
                      <tr key={user.id}>
                        <td>{user.username}</td>
                        <td>{user.password_hash}</td>
                        <td>{user.created_at}</td>
                      </tr>
                    ))
                  )
                
                }
                    
                   

                
            </tbody>
        </table>
        </>
    )
}

export default Dashboard