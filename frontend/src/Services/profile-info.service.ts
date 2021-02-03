import { Profile } from "./../Entities/profile";
import { request, RepositoryResponse } from "./repository";

const URL_API_PROFILE_INFO = "/api/profile";

export interface ServiceResponse {
  status: "OK" | "ERROR";
  data?: Profile;
  error?: string;
}

export async function getInfo(): Promise<ServiceResponse> {
  const method = "GET";

  const options = {
    method,
  };

  const response: RepositoryResponse = await request(
    URL_API_PROFILE_INFO,
    options
  );

  if (response.status === "OK") {
    const data = response.data;
    return {
      status: "OK",
      data,
    };
  }

  return {
    status: "ERROR",
    error: response.data.error,
  };
}
