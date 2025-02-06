import { NavigateFunction } from "react-router-dom";

let navigate: NavigateFunction;
export const setNavigate = (navigateFn: NavigateFunction) => {
  navigate = navigateFn;
};

export const navigateTo = (path: string) => {
  if (navigate) navigate(path);
};
