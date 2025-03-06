export interface NavbarProfileInfo {
    phone: string;
    pictureUrl: string | null;
  }
  
  export const alertTypes = ["error", "info", "success", "warning"] as const;
  export type AlertType = typeof alertTypes[number];
  
  export interface AlertData {
    message: string;
    type: AlertType;
  }