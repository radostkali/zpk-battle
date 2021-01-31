import React, { useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { getInfo } from "../../Services/profile-info.service";
import { useStore } from "../../Store";
import { LoginPage } from "../LoginPage/LoginPage";
import { MainPage } from "../MainPage/MainPage";
import "./App.css";

function App() {
  const store = useStore();
  const navigate = useNavigate();

  useEffect(() => {
    onLoad();
  }, []);

  const onLoad = async () => {
    const serverResponse = await getInfo();
    if (serverResponse.status === "OK") {
      const { id, username } = serverResponse.data!;
      store.login(id, username);
    } else {
      store.logout();
      navigate("/login");
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
