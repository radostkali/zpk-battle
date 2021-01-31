import { observer } from "mobx-react-lite";
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../../Services/logout.service";
import { useStore } from "../../Store";
import "./MainPage.css";

export const MainPage = observer(() => {
  const store = useStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!store.isAuth) {
      navigate("/login");
    }
  }, [store.isAuth]);

  const logoutHandler = async (e: React.MouseEvent<HTMLButtonElement>) => {
    await logout();
    store.logout();
  };

  return (
    <div>
      <header className="header">
        <span className="header__username">{store.username}</span>
        <button className="header__logout-btn" onClick={logoutHandler}>
          Log Out
        </button>
      </header>
      <div className="body">
        
      </div>
    </div>
  );
});
