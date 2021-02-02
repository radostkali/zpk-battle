import { request, RepositoryResponse } from "./repository";

const URL_API_SUBMIT_TRACK = "/api/submit-track";

export interface ServiceResponse {
  status: "OK" | "ERROR";
  error?: string;
}

export async function submitTrack(
  roundId: number,
  name: string
): Promise<ServiceResponse> {
  const data = {
    roundId,
    name,
  };
  const body = JSON.stringify(data);
  const method = "POST";

  const options = {
    method,
    body,
  };

  const response: RepositoryResponse = await request(
    URL_API_SUBMIT_TRACK,
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
