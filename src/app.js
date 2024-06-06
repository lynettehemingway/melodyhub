import React, { useEffect } from 'react';

import Header from "./components/header/header";
import Footer from "./components/footer/footer"
import Home from './pages/home/home';

function App() {
  return (
    <BrowserRouter>
      <RedirectHandler />
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
    
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;