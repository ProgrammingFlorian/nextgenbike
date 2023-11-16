import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Homepage from './pages/Homepage.jsx'
import Trips from "./pages/Trips.jsx"
import TripDetail from './pages/TripDetail.jsx'
import './index.css'

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <Homepage />,
      },
      {
        path: "/trips",
        element: <Trips />,
      },
      {
        path: "/trips/:id",
        element: <TripDetail />,
      }
    ]
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
