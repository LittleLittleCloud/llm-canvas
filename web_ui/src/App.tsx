import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { Header } from "./components/Header";
import { ThemeProvider } from "./components/ThemeProvider";
import "./index.css";
import { CanvasPage } from "./pages/CanvasPage";
import { DocumentationPage } from "./pages/DocumentationPage";
import { GalleryPage } from "./pages/GalleryPage";

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <Router>
        <div className="flex flex-col h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-200">
          <Header />
          <div className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<GalleryPage />} />
              <Route path="/canvas/:id" element={<CanvasPage />} />
              <Route path="/docs" element={<DocumentationPage />} />
              <Route
                path="*"
                element={
                  <div className="flex-1 flex items-center justify-center text-gray-500 dark:text-gray-400">
                    Page not found
                  </div>
                }
              />
            </Routes>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  );
};

export default App;
