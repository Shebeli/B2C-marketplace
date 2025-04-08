import errorMessages from "./errorMessages";
import queryString from "query-string";

export type FailedResponse = {
  status: number;
  userMessage: string;
  details: string;
};

/**
 * Helper function to check if the response follows the structure of type FailedResponse
 */
export const isFailedResponse = (errorDetails: object) => {
  return (
    errorDetails &&
    "status" in errorDetails &&
    "userMessage" in errorDetails &&
    "details" in errorDetails
  );
};

/**
 * A generic type for API responses recieved from backend routes.
 * T represents the expected data structure in the response body.
 */
export type ApiResponse<T> = T;

/**
 * Options to be passed to fetch, when using one of API methods, this format
 * should be followed for options.
 */
interface FetchOptions extends RequestInit {
  timeout?: number;
  revalidate?: number | false; // caching
  params?: Record<string, unknown>;
}

export const createFetchClient = (
  baseUrl: string,
  defaultOptions: FetchOptions = {}
) => {
  const defaultTimeout = defaultOptions.timeout || 10000;

  async function fetchApi<T>(
    endpoint: string,
    options: FetchOptions = {}
  ): Promise<ApiResponse<T> | FailedResponse> {
    const timeoutMs = options.timeout || defaultTimeout;
    const params = options.params || {};
    const revalidate = options.revalidate ?? defaultOptions.revalidate;

    // Construct URL
    let url = `${baseUrl}${endpoint}`;

    if (Object.keys(params).length > 0) {
      const queryStr = queryString.stringify(params, {
        arrayFormat: "comma",
      });
      url = `${url}${url.includes("?") ? "&" : "?"}${queryStr}`;
    }
    try {
      // setup abort controller
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

      const fetchOptions: RequestInit = {
        ...defaultOptions,
        ...options,
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          ...defaultOptions.headers,
          ...options.headers,
        },
      };

      if (typeof revalidate === "number") {
        fetchOptions.next = { revalidate };
      }

      const response = await fetch(url, fetchOptions);
      clearTimeout(timeoutId);

      if (!response.ok) {
        return {
          status: response.status,
          userMessage:
            response.status in errorMessages
              ? errorMessages[response.status]
              : "یک خطایی غیر منتظره از سمت سرور رخ داده است, لطفا بعدا تلاش کنید.",
          details: response.statusText,
        };
      }

      const resJson = await response.json();
      return resJson;
    } catch (error) {
      console.error(
        `An unexpected error has happened when fetching ${endpoint}`,
        error
      );

      if (error instanceof DOMException && error.name === "AbortError") {
        return {
          status: 408, // timeout
          userMessage: errorMessages[408],
          details: error.message,
        };
      }

      return {
        status: 500,
        userMessage: errorMessages[500],
        details:
          error instanceof Error ? error.message : "Unknown type of error",
      };
    }
  }

  return {
    get: <T>(
      endpoint: string,
      options?: FetchOptions
    ): Promise<ApiResponse<T> | FailedResponse> =>
      fetchApi<T>(endpoint, { method: "GET", ...options }),

    post: <T>(
      endpoint: string,
      data?: object,
      options?: FetchOptions
    ): Promise<ApiResponse<T> | FailedResponse> =>
      fetchApi<T>(endpoint, {
        method: "POST",
        body: JSON.stringify(data),
        ...options,
      }),

    put: <T>(
      endpoint: string,
      data?: object,
      options?: FetchOptions
    ): Promise<ApiResponse<T> | FailedResponse> =>
      fetchApi<T>(endpoint, {
        method: "PUT",
        body: JSON.stringify(data),
        ...options,
      }),

    delete: <T>(
      endpoint: string,
      options?: FetchOptions
    ): Promise<ApiResponse<T> | FailedResponse> =>
      fetchApi<T>(endpoint, {
        method: "DELETE",
        ...options,
      }),
  };
};

export const api = createFetchClient(
  process.env.API_BASE_URL || "http://localhost:8000"
);
