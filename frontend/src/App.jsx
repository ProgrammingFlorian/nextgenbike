import Navbar from "./components/Navbar";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <>
      <Outlet />
      <Navbar />
    </>
  );
}

export default App;
