import { observer } from "mobx-react-lite";
import React, { useState } from "react";
import { submitTrack } from "../../Services/submit-track.service";
import { useStore } from "../../Store";
import { RoundTable } from "../RoundTable/RoundTable";
import "./RoundBlock.css";

export const RoundBlock: React.FC<
  React.PropsWithoutRef<{ roundId: number }>
> = observer(({ roundId }) => {
  const [showSubmitTrackForm, setShowSubmitTrackForm] = useState<boolean>(
    false
  );
  const [newTrackName, setNewTrackName] = useState<string>("");
  const [submitTrackError, setSubmitTrackError] = useState<string | null>(null);
  const store = useStore();

  const round = store.getRound(roundId);
  const roundHasMyTrack = round!.tracks.find((x) => x.userId === store.id);

  const dateLocalizeOptions = {
    day: "numeric",
    month: "long",
    year: "numeric",
  };
  const lastDay: Date = new Date(round?.lastDay!);
  const lastDateLocalized = lastDay.toLocaleDateString(
    "en-US",
    dateLocalizeOptions
  );

  const submitBtn =
    store.isAuth &&
    !roundHasMyTrack &&
    !showSubmitTrackForm &&
    !round!.isExpired ? (
      <button
        className="round__submit-btn"
        onClick={() => {
          setShowSubmitTrackForm(true);
        }}
      >
        Сдать трэк
      </button>
    ) : null;

  const submitHandler = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const serviceResponse = await submitTrack(roundId, newTrackName);
    if (serviceResponse.status === "OK") {
      window.location.reload();
    } else {
      setSubmitTrackError(serviceResponse.error!);
    }
  };

  const submitTrackForm = showSubmitTrackForm && (
    <form className="round__submit-track-form" onSubmit={submitHandler}>
      <input
        className="round__submit-track-form-input"
        type="text"
        required
        placeholder="Название трэка"
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
          setNewTrackName(e.target.value);
        }}
      ></input>
      <span className="round__submit-track-error">{submitTrackError}</span>
      <button className="round__submit-btn">Подтвердить</button>
    </form>
  );

  const roundStyle = round?.style ? (
    <span className="round__title_style">{round?.style}</span>
  ) : null;

  const roundTable = round?.tracks.length ? (
    <RoundTable roundId={roundId} />
  ) : (
    <span className="round__no-tracks">Ждем первого участника...</span>
  );

  return (
    <div className="round">
      <div className="round__header">
        <div className="round__title">
          <span className="round__title_number">Раунд #{round?.number}</span>{" "}
          <span className="round__title_theme">{round?.theme}</span>{" "}
          {roundStyle}
        </div>
        <span className="round__last-date">
          Прием трэков до {lastDateLocalized}
        </span>
      </div>
      {roundTable}
      <div className="round__submit-track">
        {submitBtn}
        {submitTrackForm}
      </div>
    </div>
  );
});
