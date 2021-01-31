import { request, RepositoryResponse } from "./repository";

const URL_API_AUTH_LOGIN = "/api/logout";

export interface ServiceResponse {
  status: "OK" | "ERROR";
  error?: string;
}

export async function logout(): Promise<ServiceResponse> {
  const method = "POST";

  const options = {
    method,
  };

  const response: RepositoryResponse = await request(
    URL_API_AUTH_LOGIN,
    options
  );

  if (response.status === "OK") {
    return {
      status: "OK",
    };
  }

  return {
    status: "ERROR",
    error: response.data.error,
  };
}
