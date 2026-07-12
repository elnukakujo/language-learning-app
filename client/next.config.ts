import type { NextConfig } from "next";

const nextConfig = {
  // Reuse the server's LAPP_HOST/LAPP_PORT (root .env) as browser-visible vars,
  // instead of duplicating them under NEXT_PUBLIC_ names in .env.example.
  env: {
    NEXT_PUBLIC_LAPP_HOST: process.env.LAPP_HOST,
    NEXT_PUBLIC_LAPP_PORT: process.env.LAPP_PORT,
  },
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '5000',
        pathname: '/media/images/**',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '5000',
        pathname: '/media_dev/images/**',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '5000',
        pathname: '/media_test/images/**',
      },
    ],
  },
} as NextConfig;

export default nextConfig;
