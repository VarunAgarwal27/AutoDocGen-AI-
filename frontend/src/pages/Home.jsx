import { useNavigate } from "react-router-dom";

function Home() {

  const navigate = useNavigate();

  return (
    <div>

      {/* Navbar */}
      <nav className="navbar navbar-light bg-light px-4">
        <h4>AutoDocGen</h4>

        <div>
          <button
            className="btn btn-outline-primary me-2"
            onClick={() => navigate("/login")}
          >
            Login
          </button>

          <button
            className="btn btn-primary"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
        </div>
      </nav>


      {/* Hero Section */}
      <div className="container text-center mt-5">

        <h1>Generate Documentation for Any Codebase Instantly</h1>

        <p className="mt-3">
          Upload your GitHub repository or ZIP file and AutoDocGen will
          automatically generate architecture diagrams, module explanations,
          and documentation using AI.
        </p>

      </div>


      {/* Upload Section */}
      <div className="container mt-5">

        <div className="card p-4 shadow">

          <h4>Upload Repository</h4>

          <input
            type="text"
            placeholder="Paste GitHub Repository Link"
            className="form-control mt-3"
            disabled
          />

          <p className="text-center mt-3">OR</p>

          <input
            type="file"
            className="form-control"
            disabled
          />

          <button
            className="btn btn-success mt-3"
            onClick={() => navigate("/login")}
          >
            Login to Generate Documentation
          </button>

        </div>

      </div>

    </div>
  );
}

export default Home;