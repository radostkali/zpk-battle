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

  const submitBtn =
    store.isAuth && !roundHasMyTrack && !showSubmitTrackForm ? (
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

  const options = { day: "numeric", month: "long", year: "numeric" };
  const date = new Date(round?.lastDay!).toLocaleDateString("en-US", options);

  return (
    <div className="round">
      <div className="round__header">
        <div className="round__title">
          <span className="round__title_number">Раунд #{round?.number}</span>{" "}
          <span className="round__title_theme">{round?.theme}</span>{" "}
          {roundStyle}
        </div>
        <span className="round__last-date">Прием трэков до {date}</span>
      </div>
      <RoundTable roundId={roundId} />
      <div className="round__submit-track">
        {submitBtn}
        {submitTrackForm}
      </div>
    </div>
  );
});