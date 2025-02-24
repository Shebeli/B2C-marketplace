"use client";

import { useEffect, useState } from "react";
import { alertTypes } from "@/app/lib/constants";
import React from "react";
import clsx from "clsx";
import { SuccessIcon, WarningIcon, InfoIcon, ErrorIcon } from "./alertIcons";
import toast from "react-hot-toast";

export interface AlertProps {
  message: string;
  type: (typeof alertTypes)[number];
  duration?: number;
  trigger?: number;
}

const iconMap = {
  success: <SuccessIcon />,
  error: <ErrorIcon />,
  warning: <WarningIcon />,
  info: <InfoIcon />,
};

// Deprecated
export const Alert: React.FC<AlertProps> = ({
  message,
  type,
  duration = 4000,
  trigger = 0,
}) => {
  const [isVisible, setIsVisible] = useState<boolean>(true);
  const [alertData, setAlertData] = useState({ message, type });

  useEffect(() => {
    // this check only nulifies if the message is "", so the alert can be cleared.
    if (message) {
      setAlertData({ message, type });
      setIsVisible(true);

      const timeout = setTimeout(() => {
        setIsVisible(false);
      }, duration);
      return () => clearTimeout(timeout);
    }
  }, [message, type, duration, trigger]);

  if (!isVisible) return null;

  return (
    <div
      className={clsx(
        "alert p-3 self-center w-fit mx-2 flex fixed top-5 shadow-lg transition-all duration-300 ease-in-out transform",
        isVisible
          ? "opacity-100 scale-100 translate-y-0"
          : "opacity-0 scale-95 -translate-y-5",
        {
          "alert-error": alertData.type === "error",
          "alert-success": alertData.type === "success",
          "alert-info": alertData.type === "info",
          "alert-warning": alertData.type === "warning",
        }
      )}
    >
      {iconMap[alertData.type]}
      <span>{alertData.message}</span>
    </div>
  );
};

export function toastCustom(
  message: string,
  type: (typeof alertTypes)[number]
) {
  toast.custom((t) => (
    <div
      role="alert"
      className={`alert alert-${type} flex flex-row text-sm p-3 w-fit mx-2 ${
        t.visible ? "animate-enter" : "animate-leave"
      }`}
    >
      {iconMap[type]}
      <span>{message}</span>
    </div>
  ));
}

export default Alert;
