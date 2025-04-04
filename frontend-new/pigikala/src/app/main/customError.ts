/**
 * For response errors received from the backend.
 */
export class ApiError extends Error {
  status: number; // API error code
  userMessage: string; // message to be displayed to users
  details: string;

  constructor({
    status,
    details,
    userMessage,
  }: {
    status: number;
    details: string;
    userMessage: string;
  }) {
    super(
      JSON.stringify({
        status: status,
        userMessage: userMessage,
        type: "ApiError",
      })
    );
    this.details = details;
    this.status = status;
    this.userMessage = userMessage;
    this.name = "ApiError";
  }
}

/**
 * Error due to invalid query params. Reset button should be provided to reset query params.
 */
export class QueryParamError extends Error {
  status: number;
  userMessage: string;
  details: string;

  constructor({ details }: { details: string }) {
    const errorMsg =
      "پارامتر های ورودی معتبر نیست! اقدام به ریست پارامتر ها کنید! 😕";
    super(
      JSON.stringify({
        status: 400,
        userMessage: errorMsg,
        type: "QueryParamError",
      })
    );
    this.userMessage = errorMsg;
    this.status = 400;
    this.details = details;
    this.name = "QueryParamError";
  }
}
