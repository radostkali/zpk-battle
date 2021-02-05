import { observer } from "mobx-react-lite";
import React from "react";
import { fetchBattleData } from "../../Services/fetch-page-data.service";
import { toggleRate } from "../../Services/toogle-rate.service";
import { useStore } from "../../Store";
import "./RoundTable.css";

export const RoundTable: React.FC<
  React.PropsWithoutRef<{ roundId: number }>
> = observer(({ roundId }) => {
  const store = useStore();
  const round = store.getRound(roundId);

  const rateToggleHandler = async (
    roundId: number,
    categoryId: number,
    trackId: number
  ) => {
    if (!store.isAuth) {
      return;
    }

    const serviceResponse = await toggleRate(roundId, categoryId, trackId);
    if (serviceResponse.status === "OK") {
      const serviceResponse = await fetchBattleData();
      if (serviceResponse.status === "OK") {
        const { categories, rounds } = serviceResponse.data!;
        store.updateBattleData(rounds, categories);
      } else {
        console.log(serviceResponse.error);
      }
    } else {
      console.log(serviceResponse.error!);
    }
  };

  const headers = round!.tracks.map((track) => {
    return (
      <div className="round-table__item">
        <span
          className="round-table__username"
          style={{ color: track.userColor }}
        >
          {track.userUsername}
        </span>
        <span className="round-table__track-name">{track.name}</span>
      </div>
    );
  });

  const rows = store.categories.map((category) => {
    const rates = round!.tracks.map((track) => {
      const rates = track.rates.filter((x) => x.categoryId === category.id);

      const marks = rates.map((rate) => {
        const markColorStyle = { color: rate.userColor };
        return (
          <span
            className="round-table__rate"
            style={markColorStyle}
            title={rate.userUsername}
          >
            +
          </span>
        );
      });

      return (
        <div
          className="round-table__item round-table__item-rate"
          onClick={() => {
            rateToggleHandler(roundId, category.id, track.id);
          }}
        >
          {marks}
        </div>
      );
    });
    return (
      <div className="round-table__row">
        <div className="round-table__category">{category.name}</div>
        {rates}
      </div>
    );
  });

  const totalRates = round!.tracks.map((track) => {
    const total = track.rates.length;
    return (
      <div className="round-table__item round-table__total-rates">{total}</div>
    );
  });

  return (
    <div className="round-table-block">
      <div className="round-table">
        <div className="round-table__row-header">
          <div className="round-table__category"></div>
          {headers}
        </div>
        {rows}
        <div className="round-table__row">
          <div className="round-table__category"></div>
          {totalRates}
        </div>
      </div>
    </div>
  );
});
