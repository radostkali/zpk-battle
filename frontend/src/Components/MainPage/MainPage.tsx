import { observer } from "mobx-react-lite";
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { fetchBattleData } from "../../Services/fetch-page-data.service";
import { logout } from "../../Services/logout.service";
import { useStore } from "../../Store";
import { RoundBlock } from "../RoundBlock/RoundBlock";
import "./MainPage.css";

export const MainPage = observer(() => {
  const store = useStore();
  const navigate = useNavigate();

  const fetchPageData = async () => {
    const serviceResponse = await fetchBattleData();
    if (serviceResponse.status === "OK") {
      const { categories, rounds } = serviceResponse.data!;
      store.updateBattleData(rounds, categories);
    } else {
      console.log(serviceResponse.error);
    }
  };

  useEffect(() => {
    fetchPageData();
  }, []);

  const logoutHandler = async (e: React.MouseEvent<HTMLButtonElement>) => {
    await logout();
    store.logout();
  };

  const logoutBtn: React.ReactNode = (
    <button className="header__btn" onClick={logoutHandler}>
      Log Out
    </button>
  );

  const loginHandler = () => {
    navigate("/login");
  };

  const loginBtn: React.ReactNode = (
    <button className="header__btn" onClick={loginHandler}>
      Log In
    </button>
  );

  const authBtn: React.ReactNode = store.isAuth ? logoutBtn : loginBtn;

  const rounds = store.rounds.map((round, index) => {
    return (
      <div key={index}>
        <RoundBlock roundId={round.id} />
      </div>
    );
  });

  return (
    <div>
      <header className="header">
        <div>
          <span className="header__logo">ZPK онлайн рэп батл</span>
        </div>
        <div>
          <span className="header__username" style={{ color: store.color! }}>
            {store.username}
          </span>
          {authBtn}
        </div>
      </header>
      <div className="body">{rounds}</div>
    </div>
  );
});
