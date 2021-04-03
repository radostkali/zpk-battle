import { observer } from "mobx-react-lite";
import React from "react";
import { Track } from "../../Entities/battle-entities";
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

  const trackToHeaderReactElement = (
    track: Track,
    index: number
  ): React.ReactElement => {
    return (
      <div className="round-table__item" key={index}>
        <span
          className="round-table__username"
          style={{ color: track.userColor }}
        >
          {track.userUsername}
        </span>
        <span className="round-table__track-name">{track.name}</span>
      </div>
    );
  };

  let headers: React.ReactElement[] = [];

  if (round!.type === "one_vs_one") {
    round!.pairs.map((pair, pairIndex) => {
      const pairHeaders = pair.tracks.map((track, trackIndex) => {
        const uniqueIndex = pairIndex * 100 + trackIndex;
        return trackToHeaderReactElement(track, uniqueIndex);
      });
      headers = [...headers, ...pairHeaders];
    });
  } else {
    headers = round!.tracks.map((track, trackIndex) =>
      trackToHeaderReactElement(track, trackIndex)
    );
  }

  const trackToRatesReactElement = (
    track: Track,
    trackIndex: number,
    categoryId: number
  ) => {
    const rates = track.rates.filter((x) => x.categoryId === categoryId);

    const marks = rates.map((rate, rateIndex) => {
      const markColorStyle = { color: rate.userColor };
      return (
        <span
          className="round-table__rate"
          style={markColorStyle}
          title={rate.userUsername}
          key={rateIndex}
        >
          +
        </span>
      );
    });

    return (
      <div
        className="round-table__item round-table__item-rate"
        onClick={() => {
          rateToggleHandler(roundId, categoryId, track.id);
        }}
        key={trackIndex}
      >
        {marks}
      </div>
    );
  };

  const rows = store.categories.map((category, categoryIndex) => {
    let rates: React.ReactElement[] = [];
    if (round!.type === "one_vs_one") {
      round!.pairs.map((pair, pairIndex) => {
        const pairTracks = pair.tracks.map((track, trackIndex) => {
          const uniqueIndex = pairIndex * 100 + trackIndex;
          return trackToRatesReactElement(track, uniqueIndex, category.id);
        });
        rates = [...rates, ...pairTracks];
      });
    } else {
      rates = round!.tracks.map((track, trackIndex) =>
        trackToRatesReactElement(track, trackIndex, category.id)
      );
    }

    return (
      <div className="round-table__row" key={categoryIndex}>
        <div className="round-table__category">{category.name}</div>
        {rates}
      </div>
    );
  });

  let totalRates: React.ReactElement[] = [];
  if (round?.type === "one_vs_one") {
    for (let i = 0; i < round.pairs.length; i++) {
      const tracks = round.pairs[i].tracks;
      for (let j = 0; j < tracks.length; j++) {
        const total = tracks[j].rates.length;
        totalRates.push(
          <div className="round-table__item round-table__total-rates">
            {total}
          </div>
        );
      }
    }
  } else {
    totalRates = round!.tracks.map((track, index) => {
      const total = track.rates.length;
      return (
        <div className="round-table__item round-table__total-rates" key={index}>
          {total}
        </div>
      );
    });
  }

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
