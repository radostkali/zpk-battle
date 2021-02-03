import React, { useState } from "react";
import "./LoginPage.css";
import { useNavigate } from "react-router-dom";
import { login, ServiceResponse } from "../../Services/login.service";
import { useStore } from "../../Store";

type FormInput = {
  name: string;
  placeholder: string;
  type: string;
  changeHook(e: React.ChangeEvent<HTMLInputElement>): void;
};

export const LoginPage = () => {
  const store = useStore();
  const navigate = useNavigate();
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  const submitLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const serviceResponse: ServiceResponse = await login(username, password);

    if (serviceResponse.status === "OK") {
      const { id, username, color } = serviceResponse.data!;
      store.login(id, username, color);
      navigate("/");
    } else {
      setError(serviceResponse.error!);
    }
  };

  const formInputs: FormInput[] = [
    {
      name: "username",
      placeholder: "Username",
      type: "text",
      changeHook: (e: React.ChangeEvent<HTMLInputElement>) =>
        setUsername(e.target.value),
    },
    {
      name: "password",
      placeholder: "Password",
      type: "password",
      changeHook: (e: React.ChangeEvent<HTMLInputElement>) =>
        setPassword(e.target.value),
    },
  ];

  const inputNodes: React.ReactElement[] = formInputs.map(
    (inputObject: FormInput, index: number): React.ReactElement => {
      const { name, placeholder, type, changeHook } = inputObject;

      return (
        <div className="login-form__input-block" key={index}>
          <input
            required
            type={type}
            name={name}
            placeholder={placeholder}
            onChange={changeHook}
            className="login-form__input"
          />
        </div>
      );
    }
  );

  return (
    <div className="form-container">
      <h1>Enter ZPK</h1>
      <form className="login-form" onSubmit={submitLogin}>
        {inputNodes}
        <span className="login-form__error">{error}</span>
        <button className="login-form__button">Log In</button>
      </form>
    </div>
  );
};
