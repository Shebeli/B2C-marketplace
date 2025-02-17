export interface NavbarProfileInfo {
  phone: string;
  pictureUrl: string | null;
}

export const alertTypes = ["error", "info", "success", "warning"] as const;

export interface AlertData {
  message: string;
  type: (typeof alertTypes)[number];
}

export const usernamePattern =
  /^(?=[a-zA-Z])(?=(?:[^a-zA-Z]*[a-zA-Z]){3})\w{4,}$/;
