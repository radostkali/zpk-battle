import { Category, Round } from "./../Entities/battle-entities";
import { request, RepositoryResponse } from "./repository";

const URL_API_FETCH_BATTLE_DATA = "/api/battle-data";

type BattleData = {
  categories: Category[];
  rounds: Round[];
};

export interface ServiceResponse {
  status: "OK" | "ERROR";
  data?: BattleData;
  error?: string;
}

export async function fetchBattleData(): Promise<ServiceResponse> {
  const method = "GET";

  const options = {
    method,
  };

  const response: RepositoryResponse = await request(
    URL_API_FETCH_BATTLE_DATA,
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
