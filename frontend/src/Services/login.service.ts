import { Profile } from './../Entities/profile';
import { request, RepositoryResponse } from "./repository";

const URL_API_AUTH_LOGIN = "/api/login";

export interface ServiceResponse {
  status: "OK" | "ERROR";
  data?: Profile;
  error?: string;
}

export async function login(
  username: string,
  password: string
): Promise<ServiceResponse> {
  const data = {
    username,
    password,
  };
  const body = JSON.stringify(data);
  const method = "POST";

  const options = {
    method,
    body,
  };

  const response: RepositoryResponse = await request(
    URL_API_AUTH_LOGIN,
    options
  );

  if (response.status === "OK") {
    const data = response.data;
    return {
      status: "OK",
      data
    };
  }

  return {
    status: "ERROR",
    error: response.data.error,
  };
}
