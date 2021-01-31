import { makeAutoObservable } from "mobx";
import React, { useContext } from "react";

class Store {
  id: number | null = null;
  username: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  login(id: number, username: string): void {
    this.id = id;
    this.username = username;
  }

  logout(): void {
    this.id = null;
    this.username = null;
  }

  get isAuth(): boolean {
    return this.id ? true : false;
  }
}

const StoreContext = React.createContext<Store>({} as Store);

const store = new Store();

const StoreProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  return (
    <StoreContext.Provider value={store}>{children}</StoreContext.Provider>
  );
};

const useStore = () => useContext(StoreContext);

export { StoreProvider, useStore };
