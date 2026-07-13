import type { NextConfig } from "next";

// Browser-facing host/port: LAPP_HOST/LAPP_PORT is the Flask *bind* address (can be
// 0.0.0.0), which browsers can't fetch - LAPP_PUBLIC_HOST/PORT overrides it when they differ.
const publicHost = process.env.LAPP_PUBLIC_HOST || process.env.LAPP_HOST;
const publicPort = process.env.LAPP_PUBLIC_PORT || process.env.LAPP_PORT;

const nextConfig = {
  env: {
    NEXT_PUBLIC_LAPP_HOST: publicHost,
    NEXT_PUBLIC_LAPP_PORT: publicPort,
  },
  images: {
    remotePatterns: ['/media/images/**', '/media_dev/images/**', '/media_test/images/**'].map(
      (pathname) => ({
        protocol: 'http' as const,
        hostname: publicHost || '127.0.0.1',
        port: publicPort || '5000',
        pathname,
      })
    ),
  },
} as NextConfig;

export default nextConfig;
