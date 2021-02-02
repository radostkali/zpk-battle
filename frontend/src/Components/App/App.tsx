import React, { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import { getInfo } from "../../Services/profile-info.service";
import { useStore } from "../../Store";
import { LoginPage } from "../LoginPage/LoginPage";
import { MainPage } from "../MainPage/MainPage";
import "./App.css";

function App() {
  const store = useStore();

  useEffect(() => {
    onLoad();
  }, []);

  const onLoad = async () => {
    const serviceResponse = await getInfo();
    if (serviceResponse.status === "OK") {
      const { id, username } = serviceResponse.data!;
      store.login(id, username);
    } else {
      store.logout();
    }
  };

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </div>
  );
}

export default App;
