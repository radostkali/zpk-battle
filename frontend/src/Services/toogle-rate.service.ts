import { request, RepositoryResponse } from "./repository";

const URL_API_TOGGLE_RATE = "/api/toggle-rate";

export interface ServiceResponse {
  status: "OK" | "ERROR";
  error?: string;
}

export async function toggleRate(
  roundId: number,
  categoryId: number,
  trackId: number
): Promise<ServiceResponse> {
  const data = {
    roundId,
    categoryId,
    trackId,
  };
  const body = JSON.stringify(data);
  const method = "POST";

  const options = {
    method,
    body,
  };

  const response: RepositoryResponse = await request(
    URL_API_TOGGLE_RATE,
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
