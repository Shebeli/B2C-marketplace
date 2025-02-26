import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    ACCESS_TOKEN_LIFETIME: process.env.ACCESS_TOKEN_LIFETIME, //  in minutes
    REFRESH_TOKEN_LIFETIME: process.env.REFRESH_TOKEN_LIFETIME, //  in days
    API_BASE_URL: process.env.API_BASE_URL,
    CODE_REQUEST_COOLDOWN: process.env.CODE_REQUEST_COOLDOWN, // in minutes
    CODE_LIFETIME: process.env.CODE_LIFETIME, // in minutes
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "via.placeholder.com",
        port: "",
        pathname: "/300",
        search: "",
      },
    ],
  },
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 300,
        aggregateTimeout: 100,
      };
    }
    return config;
  },
};

export default nextConfig;
