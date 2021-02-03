import { makeAutoObservable } from "mobx";
import React, { useContext } from "react";
import { Category, Round } from "./Entities/battle-entities";

class Store {
  id: number | null = null;
  username: string | null = null;
  color: string | null = null;

  rounds: Round[] = [];
  categories: Category[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  login(id: number, username: string, color: string) {
    this.id = id;
    this.username = username;
    this.color = color;
  }

  logout() {
    this.id = null;
    this.username = null;
    this.color = null;
  }

  updateBattleData(rounds: Round[], categories: Category[]) {
    this.rounds = rounds;
    this.categories = categories;
  }

  get isAuth(): boolean {
    return this.id ? true : false;
  }

  getRound(id: number): Round | undefined {
    return this.rounds.find((x) => x.id === id);
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
