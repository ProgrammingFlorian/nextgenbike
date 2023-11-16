import { bike, map } from "../assets/navbar-icons";

import { Home } from "../assets/svgs";

import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="fixed w-full bottom-0 z-50 bg-white">
      <div className="grid grid-cols-3 px-4">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center p-4 gap-1 ${
              isActive ? "text-indigo-500" : "text-gray"
            }`
          }
        >
          <Home fill="gray" />
          {/* <img src={home} alt="Home" className="w-6 h-6" /> */}
          <span className="text-xs">Home</span>
        </NavLink>
        <NavLink
          to="/trips"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center p-4 gap-1 ${
              isActive ? "text-indigo-500" : "text-gray"
            }`
          }
        >
          <img src={map} alt="Map" className="w-6 h-6" />
          <span className="text-xs">Trips</span>
        </NavLink>
        <NavLink
          to="/fitness"
          className={({ isActive }) =>
            `flex flex-col items-center justify-center p-4 gap-1 ${
              isActive ? "text-indigo-500" : "text-gray"
            }`
          }
        >
          <img src={bike} alt="Bike" className="w-6 h-6" />
          <span className="text-xs">Fitness</span>
        </NavLink>
      </div>
    </nav>
  );
}
