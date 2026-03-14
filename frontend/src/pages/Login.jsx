import { useState } from "react"
import { useNavigate } from "react-router-dom"
import API from "../services/api"

function Login(){

  const navigate = useNavigate()

  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")
  const [error,setError] = useState("")

  const handleLogin = async () => {

    setError("")

    try{

      const res = await API.post("/auth/login", null, {
        params:{email,password}
      })

      localStorage.setItem("token",res.data.access_token)

      navigate("/dashboard")

    }catch(err){

      setError("Invalid email or password")

    }
  }

  return(

    <div style={{
      height:"100vh",
      display:"flex",
      justifyContent:"center",
      alignItems:"center",
      background:"#f5f7fb"
    }}>

      <div style={{
        width:"350px",
        padding:"30px",
        background:"white",
        borderRadius:"10px",
        boxShadow:"0px 5px 20px rgba(0,0,0,0.1)"
      }}>

        <h2 style={{textAlign:"center"}}>Login</h2>

        <input
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          style={{width:"100%",marginTop:"20px",padding:"10px"}}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          style={{width:"100%",marginTop:"10px",padding:"10px"}}
        />

        {error && (
          <p style={{color:"red",fontSize:"14px"}}>{error}</p>
        )}

        <button
          onClick={handleLogin}
          style={{
            width:"100%",
            marginTop:"20px",
            padding:"10px",
            background:"#4f46e5",
            color:"white",
            border:"none",
            borderRadius:"5px"
          }}
        >
          Login
        </button>

      </div>
    </div>

  )
}

export default Login