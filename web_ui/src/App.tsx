import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { Header } from "./components/Header";
import "./index.css";
import { CanvasPage } from "./pages/CanvasPage";
import { GalleryPage } from "./pages/GalleryPage";

export const App: React.FC = () => {
  return (
    <Router>
      <div className="flex flex-col h-screen">
        <Header />
        <div className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<GalleryPage />} />
            <Route path="/canvas/:id" element={<CanvasPage />} />
            <Route
              path="*"
              element={
                <div className="flex-1 flex items-center justify-center text-gray-500">
                  Page not found
                </div>
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
