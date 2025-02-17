import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    ACCESS_TOKEN_LIFESPAN: process.env.ACCESS_TOKEN_LIFESPAN,
    REFRESH_TOKEN_LIFESPAN: process.env.REFRESH_TOKEN_LIFESPAN,
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
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
};

export default nextConfig;
