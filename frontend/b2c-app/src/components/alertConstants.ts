export const alertTypes = ["error", "info", "success", "warning"] as const;

export interface Alert {
  message: string;
  type: (typeof alertTypes)[number];
}
