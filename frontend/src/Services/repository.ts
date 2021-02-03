export interface RepositoryResponse {
  status: string;
  data: any;
}

const baseFetchOptions = {
  headers: {
    "Content-Type": "application/json",
    credentials: "include",
    mode: "cors",
  },
};

export const request = async (
  url: string,
  options: {
    body?: string;
    method: string;
  }
): Promise<RepositoryResponse> => {
  options = {
    ...baseFetchOptions,
    ...options,
  };

  try {
    const response = await fetch(url, options);
    const data = await response.json();
    return {
      status: response.statusText,
      data,
    };
  } catch (error) {
    console.log(error);
    return {
      status: "Error",
      data: "Неизвестная ошибка",
    };
  }
};
