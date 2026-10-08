import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir:'./tests/ui',
  retries:0,
  use:{baseURL:process.env.BASE_URL,trace:'retain-on-failure',screenshot:'only-on-failure'},
});
