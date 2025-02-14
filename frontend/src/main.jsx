import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import './index.css';  // Make sure to import CSS here

const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement);

root.render(<App />);
